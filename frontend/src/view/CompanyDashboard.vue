<template>
  <div class="min-vh-100 bg-light">

    <CompanyNavbar
      :company="company"
      @logout="logout"
    />

    <main class="container py-4">

      <div
        v-if="loading"
        class="text-center py-5"
      >
        <div class="spinner-border text-primary"></div>
        <p class="text-muted mt-2">
          Loading dashboard...
        </p>
      </div>

      <div v-else>

        <div
          v-if="errorMessage"
          class="alert alert-danger"
        >
          {{ errorMessage }}
        </div>

        <div class="row g-4">

          <!-- Profile now takes only 5 columns -->
          <div class="col-12 col-lg-5">

            <CompanyProfile
              :company="company"
              :saving="savingProfile"
              @save="updateProfile"
            />

          </div>

          <!-- Next component will come here -->
          <div class="col-12 col-lg-7">

              <CompanyStats
                :statistics="statistics"
                :can-create-drive="canCreateDrive"
                @create-drive="openDriveForm"
              />

            </div>

        </div>
          <!-- CREATE DRIVE FORM GOES HERE -->
              <CreateDriveForm
                v-if="showDriveForm"
                :creating="creatingDrive"
                @submit="createDrive"
                @cancel="showDriveForm = false"
              />

              <DriveList
                :drives="drives"
                @manage-applicants="manageApplicants"
              />

              <ApplicantTable
                v-if="selectedDrive"
                :drive="selectedDrive"
                :applicants="applicants"
                :loading="applicantsLoading"
                @change-status="updateApplicationStatus"
                @close="selectedDrive = null"
              />

      </div>

    </main>

  </div>

</template>

<script setup>
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"

import CompanyNavbar from
  "@/components/company/CompanyNavbar.vue"

import CompanyProfile from
  "@/components/company/CompanyProfile.vue"

import CompanyStats from
  "@/components/company/CompanyStats.vue"

import CreateDriveForm from
  "@/components/company/CreateDriveForm.vue"

import DriveList from
  "@/components/company/DriveList.vue"

import ApplicantTable from
  "@/components/company/ApplicantTable.vue"
  

const router = useRouter()

const company = ref({})
const loading = ref(true)
const savingProfile = ref(false)
const errorMessage = ref("")

const drives = ref([])

const showDriveForm = ref(false)
const creatingDrive = ref(false)

const selectedDrive = ref(null)
const applicants = ref([])
const applicantsLoading = ref(false)

function openDriveForm() {
  showDriveForm.value = true
}

async function updateApplicationStatus(details) {
  const applicant = details.applicant
  const newStatus = details.newStatus

  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/company/application/${applicant.application_id}/status`,
      {
        method: "PATCH",

        headers: {
          ...getHeaders(),
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          status: newStatus
        })
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)

      await manageApplicants(selectedDrive.value)
      return
    }

    applicant.status = newStatus
  } catch (error) {
    alert("Application status could not be updated")

    await manageApplicants(selectedDrive.value)
  }
}

async function manageApplicants(drive) {
  selectedDrive.value = drive
  applicantsLoading.value = true
  applicants.value = []

  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/company/drive/${drive.id}/applicants`,
      {
        headers: getHeaders()
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    applicants.value = data.applicants
  } catch (error) {
    alert("Applicants could not be loaded")
  } finally {
    applicantsLoading.value = false
  }
}

async function fetchDrives() {
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/company/drive",
      {
        headers: getHeaders()
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(
        data.message || "Drives could not be loaded"
      )
    }

    drives.value = data.drive
  } catch (error) {
    errorMessage.value = error.message
  }
}

async function createDrive(driveData) {
  creatingDrive.value = true

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/company/drive",
      {
        method: "POST",

        headers: {
          ...getHeaders(),
          "Content-Type": "application/json"
        },

        body: JSON.stringify(driveData)
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    alert(data.message)
    showDriveForm.value = false

    await fetchCompanyDashboard()
    await fetchDrives()

  } catch (error) {
    alert("Drive could not be created")
  } finally {
    creatingDrive.value = false
  }
}

const statistics = ref({
  active_drives: 0,
  total_drives: 0,
  total_applicants: 0
})

const canCreateDrive = ref(false)

function getHeaders() {
  return {
    "Authentication-Token":
      localStorage.getItem("auth_token")
  }
}

async function fetchCompanyDashboard() {
  loading.value = true
  errorMessage.value = ""

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/company/dashboard",
      {
        headers: getHeaders()
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(
        data.message || "Dashboard could not be loaded"
      )
    }

    company.value = data.company
    statistics.value = data.statistics
    canCreateDrive.value = data.can_create_drive
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    loading.value = false
  }
}

async function updateProfile(profileData) {
  savingProfile.value = true

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/company/profile",
      {
        method: "PUT",

        headers: {
          ...getHeaders(),
          "Content-Type": "application/json"
        },

        body: JSON.stringify(profileData)
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    company.value = data.company
    alert(data.message)
  } catch (error) {
    alert("Profile could not be updated")
  } finally {
    savingProfile.value = false
  }
}

function logout() {
  localStorage.removeItem("auth_token")
  localStorage.removeItem("role")

  router.push("/login")
}

onMounted(async () => {
  await fetchCompanyDashboard()
  await fetchDrives()
})
</script>
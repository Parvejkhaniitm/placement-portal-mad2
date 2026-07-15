<template>
  <div class="min-vh-100 bg-light">
     
    <StudentNavbar
        :student="student"
        @edit-profile="openProfileForm"
        @logout="logout"
    />


    <main class="container py-4">

      <h1>
        Student Dashboard
      </h1>

      <p class="text-muted">
        View placement drives and track your applications.
      </p>

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

        <div class="alert alert-primary">
            Branch: {{ student.branch }} |
            Year: {{ student.year }}
        </div>

        <StudentProfileForm
          v-if="showProfileForm"
          :student="student"
          :saving="savingProfile"
          @save="updateProfile"
          @cancel="showProfileForm = false"
        />

          <StudentStats :statistics="statistics" />

            <AvailableDriveList
                :drives="drives"
                :can-apply="canApply"
                @view="openDriveModal"
                @apply="applyDrive"
            />

            <MyApplications
                :applications="applications"
            />

            <DriveDetailsModal
                v-if="selectedDrive"
                :drive="selectedDrive"
                :can-apply="canApply"
                @close="closeDriveModal"
                @apply="applyDriveFromModal"
            />

      </div>

    </main>

  </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"


import StudentStats from
  "@/components/student/StudentStats.vue"


import AvailableDriveList from
  "@/components/student/AvailableDriveList.vue"

import MyApplications from
  "@/components/student/MyApplications.vue"

import DriveDetailsModal from
  "@/components/student/DriveDetailsModal.vue"

import StudentNavbar from
  "@/components/student/StudentNavbar.vue"

import StudentProfileForm from
  "@/components/student/StudentProfileForm.vue"


const router = useRouter()
const student = ref({})
const statistics = ref({
  active_drives: 0,
  total_applications: 0,
  selected_applications: 0
})

const loading = ref(true)
const errorMessage = ref("")


const drives = ref([])
const canApply = ref(false)

const applications = ref([])

const selectedDrive = ref(null)

const showProfileForm = ref(false)
const savingProfile = ref(false)



async function updateProfile(profileData) {
  savingProfile.value = true

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/student/profile",
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

    student.value = data.student
    showProfileForm.value = false

    alert(data.message)

    await fetchStudentDashboard()
    await fetchDrives()
  } catch (error) {
    alert("Profile could not be updated")
  } finally {
    savingProfile.value = false
  }
}

function openProfileForm() {
  showProfileForm.value = true
}

function getHeaders() {
  return {
    "Authentication-Token":
      localStorage.getItem("auth_token")
  }
}

function logout() {
  localStorage.removeItem("auth_token")
  localStorage.removeItem("role")

  router.push("/login")
}


function openDriveModal(drive) {
  selectedDrive.value = drive
}

function closeDriveModal() {
  selectedDrive.value = null
}

async function applyDriveFromModal(driveId) {
  await applyDrive(driveId)

  selectedDrive.value = null
}



async function fetchApplications() {
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/student/applications",
      {
        headers: getHeaders()
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    applications.value = data
  } catch (error) {
    alert("Applications could not be loaded")
  }
}



async function fetchDrives() {
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/student/drives",
      {
        headers: getHeaders()
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    drives.value = data
  } catch (error) {
    alert("Drives could not be loaded")
  }
}

async function applyDrive(driveId) {
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/student/drive/${driveId}/apply`,
      {
        method: "POST",

        headers: getHeaders()
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    alert(data.message)

    await fetchStudentDashboard()
    await fetchDrives()
    await fetchApplications()

  } catch (error) {
    alert("Application could not be submitted")
  }
}

async function fetchStudentDashboard() {
  loading.value = true
  errorMessage.value = ""

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/student/dashboard",
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

    student.value = data.student
    statistics.value = data.statistics
    canApply.value = data.can_apply
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchStudentDashboard()
  await fetchDrives()
  await fetchApplications()
})

</script>
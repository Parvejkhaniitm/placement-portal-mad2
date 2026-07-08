<template>
  <div class="min-vh-100 bg-light">

    <AdminNavbar @logout="logout" />


    <CompanyDetailsModal
      v-if="selectedCompany"
      :company="selectedCompany"
      @close="closeCompanyModal"
      @approve="approveCompanyFromModal"
      @reject="rejectCompanyFromModal"
    />

    <StudentDetailsModal
      v-if="selectedStudent"
      :student="selectedStudent"
      @close="closeStudentModal"
      @blacklist="blacklistStudentFromModal"
      @reactivate="reactivateStudentFromModal"
    />

    <DriveDetailsModal
     v-if="selectedDrive"
     :drive="selectedDrive"
     @close="closeDriveModal"
     @approve="approveDriveFromModal"
     @reject="rejectDriveFromModal"
    />

    <main class="container py-4">
      <h1>Admin Dashboard</h1>

      <p class="text-muted">
        Manage the placement portal.
      </p>


       <AdminStats :stats="stats" />

       <AdminTabs
        :active-section="activeSection"
        :pending-count="stats.total_pending_company"
         @change-section="activeSection = $event"
       />
       
  <div v-if="activeSection === 'pending'">

      <PendingCompanyList
        :companies="pendingCompanies"
        :loading="companiesLoading"
        @view="openCompanyModal"
        @approve="updateCompanyStatus($event, 'approve')"
        @reject="updateCompanyStatus($event, 'reject')"
      />

      <PendingDriveList
        :drives="pendingDrives"
        @view="openDriveModal"
        @approve="updateDriveStatus($event, 'approve')"
        @reject="updateDriveStatus($event, 'reject')"
      />
</div>

      <StudentManagement
        v-if="activeSection === 'students'"
        :students="students"
        :loading="studentsLoading"
         @view="openStudentModal"
        @blacklist="updateStudentStatus($event, 'blacklist')"
        @reactivate="updateStudentStatus($event, 'reactivate')"
      />

      <CompanyManagement
        v-if="activeSection === 'companies'"
        :companies="companies"
        :loading="companiesLoading"
        @view="openCompanyModal"
        @blacklist="updateRegisteredCompany($event, 'blacklist')"
        @reactivate="updateRegisteredCompany($event, 'approve')"
      />

      <ReportsSection
        v-if="activeSection === 'reports'"
        :stats="stats"
      />

    </main>

  </div>
</template>

<script setup>
import { useRouter } from "vue-router"
import { onMounted, ref } from "vue"



import AdminNavbar from
  "@/components/admin/AdminNavbar.vue"


import AdminStats from
  "@/components/admin/AdminStats.vue"

import AdminTabs from
  "@/components/admin/AdminTabs.vue"

import PendingCompanyList from
  "@/components/admin/PendingCompanyList.vue"

import PendingDriveList from
  "@/components/admin/PendingDriveList.vue"

import StudentManagement from
  "@/components/admin/StudentManagement.vue"

import CompanyManagement from
  "@/components/admin/CompanyManagement.vue"


import CompanyDetailsModal from
  "@/components/admin/CompanyDetailsModal.vue"

import StudentDetailsModal from
  "@/components/admin/StudentDetailsModal.vue"

import DriveDetailsModal from
  "@/components/admin/DriveDetailsModal.vue"

import ReportsSection from
  "@/components/admin/ReportsSection.vue"

const router = useRouter()
const activeSection = ref("pending")
const pendingCompanies = ref([])
const companiesLoading = ref(false)
const pendingDrives = ref([])
const students = ref([])
const studentsLoading = ref(false)
const companies = ref([])
const selectedCompany = ref(null)
const selectedStudent = ref(null)
const selectedDrive = ref(null)


const stats = ref({
  total_students: 0,
  total_company: 0,
  total_drive: 0,
  total_pending_company: 0
})



function openDriveModal(drive) {
  selectedDrive.value = drive
}

function closeDriveModal() {
  selectedDrive.value = null
}

async function approveDriveFromModal(driveId) {
  await updateDriveStatus(driveId, "approve")

  selectedDrive.value = null

  await fetchPendingDrives()
  await fetchStats()
}

async function rejectDriveFromModal(driveId) {
  await updateDriveStatus(driveId, "reject")

  selectedDrive.value = null

  await fetchPendingDrives()
  await fetchStats()
}

function openStudentModal(student) {
  selectedStudent.value = student
}

function closeStudentModal() {
  selectedStudent.value = null
}

async function blacklistStudentFromModal(studentId) {
  await updateStudentStatus(studentId, "blacklist")

  selectedStudent.value = null

  await fetchStudents()
}

async function reactivateStudentFromModal(studentId) {
  await updateStudentStatus(studentId, "reactivate")

  selectedStudent.value = null

  await fetchStudents()
}


function openCompanyModal(company) {
  selectedCompany.value = company
}

function closeCompanyModal() {
  selectedCompany.value = null
}

async function approveCompanyFromModal(companyId) {
  await updateCompanyStatus(companyId, "approve")

  selectedCompany.value = null

  await fetchStats()
  await fetchPendingCompanies()
  await fetchCompanies()
}

async function rejectCompanyFromModal(companyId) {
  await updateCompanyStatus(companyId, "reject")

  selectedCompany.value = null

  await fetchStats()
  await fetchPendingCompanies()
  await fetchCompanies()
}

async function fetchCompanies() {
  companiesLoading.value = true

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/admin/company-list",
      {
        headers: {
          "Authentication-Token":
            localStorage.getItem("auth_token")
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    companies.value = data
  } catch (error) {
    alert("Companies could not be loaded")
  } finally {
    companiesLoading.value = false
  }
}

async function updateRegisteredCompany(
  companyId,
  action
) {
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/admin/company/${companyId}/${action}`,
      {
        method: "PUT",

        headers: {
          "Authentication-Token":
            localStorage.getItem("auth_token")
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    alert(data.message)

    await fetchCompanies()
    await fetchStats()
  } catch (error) {
    alert("Company status could not be updated")
  }
}


async function fetchStudents() {
  studentsLoading.value = true

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/admin/students",
      {
        headers: {
          "Authentication-Token":
            localStorage.getItem("auth_token")
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    students.value = data
  } catch (error) {
    alert("Students could not be loaded")
  } finally {
    studentsLoading.value = false
  }
}

async function updateStudentStatus(studentId, action) {
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/admin/student/${studentId}/${action}`,
      {
        method: "PUT",

        headers: {
          "Authentication-Token":
            localStorage.getItem("auth_token")
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    alert(data.message)
    await fetchStudents()
  } catch (error) {
    alert("Student status could not be updated")
  }
}




async function fetchPendingDrives() {
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/admin/pending-drives",
      {
        headers: {
          "Authentication-Token":
            localStorage.getItem("auth_token")
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    pendingDrives.value = data
  } catch (error) {
    alert("Pending drives could not be loaded")
  }
}

async function updateDriveStatus(driveId, action) {
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/admin/drive/${driveId}/${action}`,
      {
        method: "PUT",

        headers: {
          "Authentication-Token":
            localStorage.getItem("auth_token")
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    alert(data.message)

    await fetchPendingDrives()
    await fetchStats()
  } catch (error) {
    alert("Drive status could not be updated")
  }
}


async function fetchPendingCompanies() {
  companiesLoading.value = true

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/admin/pending-company",
      {
        headers: {
          "Authentication-Token":
            localStorage.getItem("auth_token")
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    pendingCompanies.value = data
  } catch (error) {
    alert("Pending companies could not be loaded")
  } finally {
    companiesLoading.value = false
  }
}

async function updateCompanyStatus(companyId, action) {
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/admin/company/${companyId}/${action}`,
      {
        method: "PUT",

        headers: {
          "Authentication-Token":
            localStorage.getItem("auth_token")
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    alert(data.message)

    await fetchPendingCompanies()
    await fetchStats()
  } catch (error) {
    alert("Company status could not be updated")
  }
}


async function fetchStats() {
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/admin/stats",
      {
        headers: {
          "Authentication-Token":
            localStorage.getItem("auth_token")
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message)
      return
    }

    stats.value = data
  } catch (error) {
    alert("Dashboard statistics could not be loaded")
  }
}


function logout() {
  localStorage.removeItem("auth_token")
  localStorage.removeItem("role")

  router.push("/login")
}

onMounted(async () => {
  await fetchStats()
  await fetchPendingCompanies()
  await fetchPendingDrives()
  await fetchStudents()
  await fetchCompanies()
})
</script>
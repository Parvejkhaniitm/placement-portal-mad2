<template>

<div class="container mt-4">

    <!-- ========================= -->
    <!-- DASHBOARD OVERVIEW -->
    <!-- ========================= -->

    <h1 class="mb-2">Dashboard Overview</h1>

    <p class="text-muted">
        Welcome Admin. Here's what's happening across the placement portal.
    </p>

    <!-- STATS CARDS -->

    <div class="row mt-4">

        <div class="col-md-4">
            <div class="card shadow-sm">
                <div class="card-body">

                    <h6 class="text-muted">
                        Total Registered Students
                    </h6>

                    <h2>
                        {{ stats.total_students }}
                    </h2>

                </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card shadow-sm">
                <div class="card-body">

                    <h6 class="text-muted">
                        Total Registered Companies
                    </h6>

                    <h2>
                        {{ stats.total_company }}
                    </h2>

                </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card shadow-sm">
                <div class="card-body">

                    <h6 class="text-muted">
                        Total Placement Drives
                    </h6>

                    <h2>
                        {{ stats.total_drive }}
                    </h2>

                </div>
            </div>
        </div>

    </div>


    <!-- ========================= -->
    <!-- MAIN ADMIN CARD -->
    <!-- ========================= -->

    <div class="card shadow-sm mt-5">

        <div class="card-header">

            <ul class="nav nav-tabs">

                <li class="nav-item">

                    <button
                        class="nav-link"
                        :class="{ active: activeSection==='pending' }"
                        @click="activeSection='pending'"
                    >
                        Pending Approvals

                        <span
                            class="badge bg-warning text-dark ms-1"
                        >
                            {{ stats.total_pending_company }}
                        </span>

                    </button>

                </li>

                <li class="nav-item">

                    <button
                        class="nav-link"
                        :class="{ active: activeSection==='users' }"
                        @click="activeSection='users'"
                    >
                        User Management
                    </button>

                </li>

                <li class="nav-item">

                    <button
                        class="nav-link"
                        :class="{ active: activeSection==='reports' }"
                        @click="activeSection='reports'"
                    >
                        Reports & Stats
                    </button>

                </li>

            </ul>

        </div>

        <div class="card-body">

            <!-- ========================= -->
            <!-- PENDING APPROVALS -->
            <!-- ========================= -->

            <div v-if="activeSection==='pending'">

                <h4 class="mb-4">
                    New Company Profiles
                </h4>

                <table class="table table-hover">

                    <thead>

                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Website</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>

                    </thead>

                    <tbody>

                    <tr
                        v-for="company in companies"
                        :key="company.id"
                    >

                        <td>{{ company.id }}</td>
                        <td>{{ company.name }}</td>
                        <td>{{ company.hr_email }}</td>
                        <td>{{ company.website }}</td>

                        <td>
                            <span class="badge bg-warning">
                                {{ company.status }}
                            </span>
                        </td>

                        <td>

                            <button
                                class="btn btn-secondary btn-sm me-2"
                            >
                                View
                            </button>

                            <button
                                class="btn btn-success btn-sm me-2"
                                @click="approveCompany(company.id)"
                            >
                                Approve
                            </button>

                            <button
                                class="btn btn-danger btn-sm"
                                @click="rejectCompany(company.id)"
                            >
                                Reject
                            </button>

                        </td>

                    </tr>

                    </tbody>

                </table>

            </div>


            <!-- ========================= -->
            <!-- USER MANAGEMENT -->
            <!-- ========================= -->

            <div v-if="activeSection==='users'">

                <div class="mb-4">

                    <button
                        class="btn me-2"
                        :class="studentTab
                            ? 'btn-primary'
                            : 'btn-outline-secondary'"
                        @click="studentTab=true"
                    >
                        Students
                    </button>

                    <button
                        class="btn"
                        :class="!studentTab
                            ? 'btn-primary'
                            : 'btn-outline-secondary'"
                        @click="studentTab=false"
                    >
                        Companies
                    </button>

                </div>

                <!-- STUDENTS -->

                <div v-if="studentTab">

                    <table class="table table-hover">

                        <thead>

                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Branch</th>
                            <th>Year</th>
                            <th>Status</th>
                            <th>Action</th>
                        </tr>

                        </thead>

                        <tbody>

                        <tr
                            v-for="student in students"
                            :key="student.id"
                        >

                            <td>{{ student.id }}</td>
                            <td>{{ student.name }}</td>
                            <td>{{ student.branch }}</td>
                            <td>{{ student.year }}</td>

                            <td>

                                <span
                                    v-if="student.status==='Active'"
                                    class="badge bg-success"
                                >
                                    Active
                                </span>

                                <span
                                    v-else
                                    class="badge bg-danger"
                                >
                                    Blacklisted
                                </span>

                            </td>

                            <td>

                                <button
                                    v-if="student.status==='Active'"
                                    class="btn btn-outline-danger btn-sm"
                                    @click="blacklistStudent(student.id)"
                                >
                                    Blacklist
                                </button>

                                <button
                                    v-else
                                    class="btn btn-outline-success btn-sm"
                                    @click="reactivateStudent(student.id)"
                                >
                                    Reactivate
                                </button>

                            </td>

                        </tr>

                        </tbody>

                    </table>

                </div>

                <!-- COMPANIES -->

                <div v-else>

                    <h5>Company Management</h5>

                    <table class="table table-hover">

                        <thead>

                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Website</th>
                            <th>Status</th>
                            <th>Action</th>
                        </tr>

                        </thead>

                        <tbody>

                        <tr
                            v-for="company in companyList"
                            :key="company.id"
                        >

                            <td>{{ company.name }}</td>
                            <td>{{ company.hr_email }}</td>
                            <td>{{ company.website }}</td>

                            <td>

                                <span
                                    v-if="company.status==='Approved'"
                                    class="badge bg-success"
                                >
                                    Approved
                                </span>

                                <span
                                    v-else
                                    class="badge bg-danger"
                                >
                                    Blacklisted
                                </span>

                            </td>
                            <td>

                                <button v-if="company.status =='Approved'" class="btn btn-outline-danger btn-sm" @click="blacklistCompany(company.id)">
                                    Deactivate
                                </button>

                                <button v-else class="btn btn-outline-success btn-sm" @click="reactivateCompany(company.id)">
                                    Reactivate
                                </button>
                            </td>

                        </tr>

                        </tbody>

                    </table>

                </div>
                

            </div>


            <!-- ========================= -->
            <!-- REPORTS -->
            <!-- ========================= -->

            <div v-if="activeSection==='reports'">

                <h3>
                    Reports & Statistics
                </h3>

                <div class="alert alert-info mt-3">
                    Reports Module Coming Soon...
                </div>

            </div>

        </div>

    </div>

</div>

</template>


<script setup>

import { ref, onMounted } from 'vue';
const companies = ref([])
const stats = ref({})
const students = ref([])
const activeSection = ref("pending")
const studentTab = ref(true)
const companyList = ref([])

const blacklistCompany = async (companyId) => {

    const token = localStorage.getItem("auth_token")
    await fetch(
        `http://127.0.0.1:5000/api/admin/company/${companyId}/blacklist`,
        {
            method: "PUT",
            headers: {
                "Authentication-Token": token
            }
        }
    )

    await fetchCompanylist()
}
const reactivateCompany = async (companyId) => {

    const token = localStorage.getItem("auth_token")

    await fetch(
        `http://127.0.0.1:5000/api/admin/company/${companyId}/approve`,
        {
            method: "PUT",
            headers: {
                "Authentication-Token": token
            }
        }
    )

    await fetchCompanylist()
}


const fetchStats = async () => {
    const token = localStorage.getItem("auth_token")
    
    const response = await fetch(
        "http://127.0.0.1:5000/api/admin/stats",
        {
            method: "GET",
            headers: {
                "Authentication-Token": token
            }
        }
    )
    const data =  await response.json()
    stats.value = data
    console.log(stats.value)
}

const fetchPendingCompanies = async () => {

    const token = localStorage.getItem("auth_token")

    const response = await fetch(
        "http://127.0.0.1:5000/api/admin/pending-company",
        {
            headers: {
                "Authentication-Token": token
            }
        }
    )
    
    const data = await response.json()
    companies.value = data
    
}
const approveCompany = async (companyId) => {
    const  token = localStorage.getItem("auth_token")

    const response = await fetch(
        `http://127.0.0.1:5000/api/admin/company/${companyId}/approve`,
        {
            method: "PUT",
            headers: {
                "Authentication-Token": token
            }
        }
    )
    const data = await response.json() 
    await fetchPendingCompanies()
    await fetchStats()
    
}

const rejectCompany = async (companyId) => {
    const token = localStorage.getItem("auth_token")

    const response = await fetch(
        `http://127.0.0.1:5000/api/admin/company/${companyId}/reject`,
        {
            method: "PUT",
            headers:{
                "Authentication-Token": token
            } 
        }

    )
    const data = await response.json()
    await fetchPendingCompanies()
    await fetchStats()

}

const fetchStudents = async () => {
    const token = localStorage.getItem("auth_token")

    const response = await fetch(
        "http://127.0.0.1:5000/api/admin/students",
        {
            headers: {
                "Authentication-Token": token
            }
        }

    )
    const data = await response.json()
    students.value = data 
}

const blacklistStudent = async (studentId) => {

    const token = localStorage.getItem("auth_token")

    await fetch(
        `http://127.0.0.1:5000/api/admin/student/${studentId}/blacklist`,
        {
            method: "PUT",
            headers: {
                "Authentication-Token": token
            }
        }
    )
    await fetchStudents()
}

const reactivateStudent = async (studentId) => {
    const token = localStorage.getItem("auth_token")

    await fetch(
        `http://127.0.0.1:5000/api/admin/student/${studentId}/reactivate`,
        {
            method: "PUT",
            headers: {
                "Authentication-Token":token
            }
        }
    )
    await fetchStudents()
}

const fetchCompanylist = async () => {

    const token = localStorage.getItem("auth_token")

    const response = await fetch(
         `http://127.0.0.1:5000/api/admin/company-list`,
         {
            method: "GET",
            headers: {
                "Authentication-Token": token
            }
         }

         
        )
    const data = await response.json()
    companyList.value = data
}



onMounted(() => {
    fetchPendingCompanies()
    fetchStats()
    fetchStudents() 
    fetchCompanylist()
})
</script>
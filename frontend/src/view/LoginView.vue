<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-12 col-md-8 col-lg-6">
        <div class="card shadow p-4">
          <div class="text-center mb-4">
            <h2 class="mb-1">Placement Portal</h2>
            <p class="text-secondary">
              University Campus Recruitment System
            </p>
          </div>

          <!-- Student / Company selection -->
          <div class="btn-group w-100 mb-4">
            <button
              type="button"
              class="btn"
              :class="selectedRole === 'student'
                ? 'btn-primary'
                : 'btn-outline-primary'"
              @click="changeRole('student')"
            >
              Student
            </button>

            <button
              type="button"
              class="btn"
              :class="selectedRole === 'company'
                ? 'btn-primary'
                : 'btn-outline-primary'"
              @click="changeRole('company')"
            >
              Company
            </button>
          </div>

          <!-- Login / Registration tabs -->
          <ul class="nav nav-tabs justify-content-center mb-4">
            <li class="nav-item">
              <button
                type="button"
                class="nav-link"
                :class="{ active: selectedTab === 'login' }"
                @click="selectedTab = 'login'"
              >
                Login
              </button>
            </li>

            <li class="nav-item">
              <button
                type="button"
                class="nav-link"
                :class="{ active: selectedTab === 'register' }"
                @click="selectedTab = 'register'"
              >
                Self-Registration
              </button>
            </li>
          </ul>

          <!-- Shared login form -->
          <LoginForm v-if="selectedTab === 'login'" />

          <!-- Student registration -->
          <StudentRegisterForm
            v-else-if="
              selectedTab === 'register' &&
              selectedRole === 'student'
            "
            @registration-success="showLogin"
          />

          <!-- Company registration -->
          <CompanyRegisterForm
            v-else
            @registration-success="showLogin"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import LoginForm from "@/components/auth/LoginForm.vue"
import StudentRegisterForm from "@/components/auth/StudentRegisterForm.vue"
import CompanyRegisterForm from "@/components/auth/CompanyRegisterForm.vue"

const selectedRole = ref("student")
const selectedTab = ref("login")

function changeRole(role) {
  selectedRole.value = role
}

function showLogin() {
  selectedTab.value = "login"
}
</script>
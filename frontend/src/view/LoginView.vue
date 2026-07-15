<template>
  <div class="min-vh-100 bg-light d-flex align-items-center py-5">
    <div class="container">

      <div class="row justify-content-center">
        <div class="col-12 col-md-9 col-lg-6">

          <div class="card border-0 shadow-lg">
            <div class="card-body p-4 p-md-5">

              <div class="text-center mb-4">
                <span class="badge bg-primary mb-2">
                  Placement Portal
                </span>

                <h1 class="h2 mb-2">
                  Welcome Back
                </h1>

                <p class="text-muted mb-0">
                  Login or register to continue
                </p>
              </div>

              <div class="btn-group w-100 mb-4">
                <button
                  type="button"
                  class="btn"
                  :class="selectedRole === 'Student'
                    ? 'btn-primary'
                    : 'btn-outline-primary'"
                  @click="changeRole('Student')"
                >
                  Student
                </button>

                <button
                  type="button"
                  class="btn"
                  :class="selectedRole === 'Company'
                    ? 'btn-primary'
                    : 'btn-outline-primary'"
                  @click="changeRole('Company')"
                >
                  Company
                </button>
              </div>

              <ul
                v-if="selectedRole !== 'admin'"
                class="nav nav-tabs justify-content-center mb-4"
              >
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

              <LoginForm
                v-if="selectedTab === 'login'"
                :expected-role="selectedRole"
              />

              <StudentRegisterForm
                v-else-if="selectedRole === 'Student'"
                @registration-success="showLogin"
              />

              <CompanyRegisterForm
                v-else-if="selectedRole === 'Company'"
                @registration-success="showLogin"
              />

              <hr class="my-4">

              <div class="text-center">
                <p class="text-muted small mb-2">
                  Are you an administrator?
                </p>

                <button
                  type="button"
                  class="btn btn-outline-dark btn-sm"
                  :class="selectedRole === 'admin'
                    ? 'active'
                    : ''"
                  @click="changeRole('admin')"
                >
                  Admin Login
                </button>
              </div>

            </div>
          </div>

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

const selectedRole = ref("Student")
const selectedTab = ref("login")

function changeRole(role) {
  selectedRole.value = role
  selectedTab.value = "login"
}

function showLogin() {
  selectedTab.value = "login"
}
</script>
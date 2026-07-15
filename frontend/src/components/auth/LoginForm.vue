<template>
  <div class="card border-0 bg-light">
    <div class="card-body p-4">

      <div class="text-center mb-4">
        <h2 class="h4 mb-1">
          {{ loginTitle }}
        </h2>

        <p class="text-muted mb-0">
          Enter your credentials to continue
        </p>
      </div>

      <form @submit.prevent="login">

        <div class="mb-3">
          <label class="form-label">
            Email
          </label>

          <input
            v-model.trim="email"
            type="email"
            class="form-control"
            placeholder="Enter email"
            @input="validateEmail"
          >

          <div class="text-danger small mt-1">
            {{ emailError }}
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">
            Password
          </label>

          <input
            v-model="password"
            type="password"
            class="form-control"
            placeholder="Enter password"
          >
        </div>

        <button
          type="submit"
          class="btn btn-primary w-100"
        >
          Login
        </button>

      </form>

    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import { useRouter } from "vue-router"

const props = defineProps({
  expectedRole: {
    type: String,
    required: true
  }
})

const router = useRouter()

const email = ref("")
const password = ref("")
const emailError = ref("")

const loginTitle = computed(() => {
  if (props.expectedRole === "admin") {
    return "Admin Login"
  }

  return `${props.expectedRole} Login`
})

function validateEmail() {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!emailPattern.test(email.value)) {
    emailError.value = "Invalid email"
    return false
  }

  emailError.value = ""
  return true
}

async function login() {
  if (!validateEmail()) {
    alert("Please enter a valid email")
    return
  }

  if (!email.value || !password.value) {
    alert("Please fill all fields")
    return
  }

  const user = {
    email: email.value,
    password: password.value
  }

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/login",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify(user)
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message || "Login failed")
      return
    }

    const role = data.user_details.Roles[0]

    if (role !== props.expectedRole) {
      alert(`Please use the ${role} login option for this account.`)
      return
    }

    localStorage.setItem(
      "auth_token",
      data.user_details.auth_token
    )

    localStorage.setItem(
      "role",
      role
    )

    if (role === "admin") {
      router.push("/admin")
      return
    }

    if (role === "Student") {
      router.push("/student")
      return
    }

    if (role === "Company") {
      router.push("/company")
    }
  } catch (error) {
    alert("Login failed. Please try again.")
  }
}
</script>
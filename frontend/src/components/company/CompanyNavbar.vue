<template>
  <nav class="navbar bg-white border-bottom px-4 py-3">

    <!-- COMPANY DETAILS -->
    <div class="d-flex align-items-center">

      <div
        class="bg-primary-subtle text-primary rounded-circle
               d-flex justify-content-center align-items-center
               me-3 p-3"
      >
        {{ companyInitial }}
      </div>

      <div>
        <h4 class="mb-1">
          {{ company.name || "Company Dashboard" }}
        </h4>

        <span
          class="badge"
          :class="statusClass"
        >
          {{ company.status || "Loading..." }}
        </span>
      </div>

    </div>

    <!-- LOGOUT BUTTON -->
    <button
      class="btn btn-outline-danger"
      @click="logout"
    >
      Logout
    </button>

  </nav>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  company: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(["logout"])

const companyInitial = computed(() => {
  if (!props.company.name) {
    return "C"
  }

  return props.company.name.charAt(0).toUpperCase()
})

const statusClass = computed(() => {
  if (props.company.status === "Approved") {
    return "bg-success"
  }

  if (props.company.status === "Rejected") {
    return "bg-danger"
  }

  if (props.company.status === "Blacklisted") {
    return "bg-danger"
  }

  return "bg-warning text-dark"
})

function logout() {
  emit("logout")
}
</script>
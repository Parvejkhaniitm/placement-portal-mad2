<template>
  <nav class="navbar navbar-light bg-white border-bottom shadow-sm">
    <div class="container-fluid px-4">

      <div class="d-flex align-items-center gap-3">

        <div
          class="rounded-circle bg-primary-subtle text-primary d-flex align-items-center justify-content-center"
          style="width: 44px; height: 44px;"
        >
          {{ studentInitial }}
        </div>

        <div>
          <h4 class="mb-0">
            {{ student.name || "Student Dashboard" }}
          </h4>

          <span
            class="badge"
            :class="student.status === 'Active'
              ? 'bg-success'
              : 'bg-danger'"
          >
            {{ student.status || "Loading..." }}
          </span>
        </div>

      </div>

      <button
        class="btn btn-outline-danger"
        @click="logout"
      >
        Logout
      </button>

    </div>
  </nav>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  student: {
    type: Object,
    required: true
  }
})

const emit = defineEmits([
  "logout"
])

const studentInitial = computed(() => {
  if (!props.student.name) {
    return "S"
  }

  return props.student.name.charAt(0).toUpperCase()
})

function logout() {
  emit("logout")
}
</script>
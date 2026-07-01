<template>
  <div class="card border-0 shadow-sm h-100">

    <div class="card-body p-4">

      <!-- TITLE AND STATUS -->
      <div class="d-flex justify-content-between align-items-start mb-2">

        <h5 class="me-2">
          {{ drive.title }}
        </h5>

        <span
          class="badge"
          :class="statusClass"
        >
          {{ drive.status }}
        </span>

      </div>

      <!-- DESCRIPTION -->
      <p class="text-muted">
        {{ drive.description }}
      </p>

      <!-- BRANCHES -->
      <p class="mb-2">
        <strong>Branches:</strong>
        {{ drive.branches.join(", ") }}
      </p>

      <!-- YEAR -->
      <p class="mb-2">
        <strong>Eligible Year:</strong>
        {{ drive.year }}
      </p>

      <!-- APPLICANTS -->
      <p class="mb-2 text-primary">
        {{ drive.applicant_count }} Applicants
      </p>

      <!-- DEADLINE -->
      <p class="small text-muted">
        Deadline: {{ formattedDeadline }}
      </p>

      <!-- MANAGE BUTTON -->
      <button
        class="btn btn-outline-primary w-100"
        @click="manageApplicants"
      >
        Manage Applicants
      </button>

    </div>

  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  drive: {
    type: Object,
    required: true
  }
})

const emit = defineEmits([
  "manage-applicants"
])

const statusClass = computed(() => {
  if (props.drive.is_active) {
    return "bg-success"
  }

  if (props.drive.status === "Pending") {
    return "bg-warning text-dark"
  }

  if (props.drive.status === "Rejected") {
    return "bg-danger"
  }

  return "bg-secondary"
})

const formattedDeadline = computed(() => {
  if (!props.drive.deadline_date) {
    return "-"
  }

  return new Date(
    props.drive.deadline_date
  ).toLocaleDateString()
})

function manageApplicants() {
  emit("manage-applicants", props.drive)
}
</script>
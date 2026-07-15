<template>
  <div class="card border-0 shadow-sm mb-4">

    <div class="card-body p-4">

      <h4 class="mb-3">
        Available Placement Drives
      </h4>

      <div
        v-if="drives.length === 0"
        class="alert alert-info mb-0"
      >
        No active placement drives are available right now.
      </div>

      <div
        v-else
        class="row g-3"
      >

        <div
          v-for="drive in drives"
          :key="drive.id"
          class="col-12 col-lg-6"
        >

          <div class="card h-100 border">

            <div class="card-body">

              <div class="d-flex justify-content-between align-items-start mb-2">

                <div>
                  <h5 class="mb-1">
                    {{ drive.title }}
                  </h5>

                  <p class="text-muted mb-0">
                    {{ drive.company_name }}
                  </p>
                </div>

                <span
                  class="badge"
                  :class="drive.is_eligible
                    ? 'bg-success'
                    : 'bg-secondary'"
                >
                  {{ drive.is_eligible ? "Eligible" : "Not Eligible" }}
                </span>

              </div>

              <p class="mb-1">
                <strong>Branches:</strong>
                {{ drive.branches.join(", ") }}
              </p>

              <p class="mb-1">
                <strong>Year:</strong>
                {{ drive.year === 0 ? "Any Year" : drive.year }}
              </p>

              <p class="mb-3">
                <strong>Deadline:</strong>
                {{ formatDate(drive.deadline_date) }}
              </p>

              <div class="d-flex gap-2">

                <button
                  class="btn btn-outline-primary btn-sm"
                  @click="viewDrive(drive)"
                >
                  View
                </button>

                <button
                  class="btn btn-primary btn-sm"
                  :disabled="
                    !drive.is_eligible ||
                    drive.already_applied ||
                    !canApply
                  "
                  @click="applyDrive(drive.id)"
                >
                  {{ drive.already_applied ? "Applied" : "Apply" }}
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
defineProps({
  drives: {
    type: Array,
    required: true
  },

  canApply: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits([
  "view",
  "apply"
])

function viewDrive(drive) {
  emit("view", drive)
}

function applyDrive(driveId) {
  emit("apply", driveId)
}

function formatDate(dateValue) {
  if (!dateValue) {
    return "-"
  }

  return new Date(dateValue).toLocaleDateString()
}
</script>
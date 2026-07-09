<template>
  <div>
    <div class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">

          <div class="modal-header">
            <h5 class="modal-title">
              Drive Details
            </h5>

            <button
              type="button"
              class="btn-close"
              @click="closeModal"
            ></button>
          </div>

          <div class="modal-body">

            <h4 class="mb-1">
              {{ drive.title }}
            </h4>

            <p class="text-muted mb-2">
              {{ drive.company_name }}
            </p>

            <span
              class="badge"
              :class="drive.is_eligible
                ? 'bg-success'
                : 'bg-secondary'"
            >
              {{ drive.is_eligible ? "Eligible" : "Not Eligible" }}
            </span>

            <hr>

            <div class="row g-3">

              <div class="col-md-6">
                <small class="text-muted">
                  Eligible Branches
                </small>

                <p class="mb-0">
                  {{ branchText }}
                </p>
              </div>

              <div class="col-md-6">
                <small class="text-muted">
                  Eligible Year
                </small>

                <p class="mb-0">
                  {{ drive.year }}
                </p>
              </div>

              <div class="col-md-6">
                <small class="text-muted">
                  Deadline
                </small>

                <p class="mb-0">
                  {{ formatDate(drive.deadline_date) }}
                </p>
              </div>

              <div class="col-md-6">
                <small class="text-muted">
                  Application Status
                </small>

                <p class="mb-0">
                  {{ drive.already_applied ? "Already Applied" : "Not Applied" }}
                </p>
              </div>

              <div class="col-12">
                <small class="text-muted">
                  Description
                </small>

                <p class="mb-0">
                  {{ drive.description }}
                </p>
              </div>

            </div>

          </div>

          <div class="modal-footer">
            <button
              class="btn btn-outline-secondary"
              @click="closeModal"
            >
              Close
            </button>

            <button
              class="btn btn-primary"
              :disabled="
                !drive.is_eligible ||
                drive.already_applied ||
                !canApply
              "
              @click="applyDrive"
            >
              {{ drive.already_applied ? "Applied" : "Apply Now" }}
            </button>
          </div>

        </div>
      </div>
    </div>

    <div class="modal-backdrop fade show"></div>
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  drive: {
    type: Object,
    required: true
  },

  canApply: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits([
  "close",
  "apply"
])

const branchText = computed(() => {
  if (!props.drive.branches) {
    return "Not provided"
  }

  return props.drive.branches.join(", ")
})

function formatDate(dateValue) {
  if (!dateValue) {
    return "-"
  }

  return new Date(dateValue).toLocaleDateString()
}

function closeModal() {
  emit("close")
}

function applyDrive() {
  emit("apply", props.drive.id)
}
</script>
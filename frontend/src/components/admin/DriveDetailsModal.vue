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

            <span
              class="badge"
              :class="statusClass"
            >
              {{ drive.status }}
            </span>

            <hr>

            <div class="row g-3">

              <div class="col-md-6">
                <small class="text-muted">Company</small>
                <p class="mb-0">
                  {{ drive.company_name || "Not provided" }}
                </p>
              </div>

              <div class="col-md-6">
                <small class="text-muted">Eligible Year</small>
                <p class="mb-0">
                  {{ drive.year || "Not provided" }}
                </p>
              </div>

              <div class="col-md-6">
                <small class="text-muted">Eligible Branches</small>
                <p class="mb-0">
                  {{ branchText }}
                </p>
              </div>

              <div class="col-md-6">
                <small class="text-muted">Deadline</small>
                <p class="mb-0">
                  {{ formatDate(drive.deadline_date) }}
                </p>
              </div>

              <div class="col-12">
                <small class="text-muted">Description</small>
                <p class="mb-0">
                  {{ drive.description || "No description provided" }}
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
              v-if="drive.status !== 'Approved'"
              class="btn btn-success"
              @click="approveDrive"
            >
              Approve Drive
            </button>

            <button
              v-if="drive.status !== 'Rejected'"
              class="btn btn-danger"
              @click="rejectDrive"
            >
              Reject Drive
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
  }
})

const emit = defineEmits([
  "close",
  "approve",
  "reject"
])

const statusClass = computed(() => {
  if (props.drive.status === "Approved") {
    return "bg-success"
  }

  if (props.drive.status === "Rejected") {
    return "bg-danger"
  }

  return "bg-warning text-dark"
})

const branchText = computed(() => {
  if (!props.drive.branches) {
    return "Not provided"
  }

  if (Array.isArray(props.drive.branches)) {
    return props.drive.branches.join(", ")
  }

  return props.drive.branches
})

function formatDate(dateValue) {
  if (!dateValue) {
    return "Not provided"
  }

  return new Date(dateValue).toLocaleDateString()
}

function closeModal() {
  emit("close")
}

function approveDrive() {
  emit("approve", props.drive.id)
}

function rejectDrive() {
  emit("reject", props.drive.id)
}
</script>
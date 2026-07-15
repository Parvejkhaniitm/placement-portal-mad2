<template>
  <div>
    <div class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">

          <div class="modal-header">
            <h5 class="modal-title">
              Company Details
            </h5>

            <button
              type="button"
              class="btn-close"
              @click="closeModal"
            ></button>
          </div>

          <div class="modal-body">

            <h4 class="mb-1">
              {{ company.name }}
            </h4>

            <span
              class="badge"
              :class="statusClass"
            >
              {{ company.status }}
            </span>

            <hr>

            <div class="row g-3">

              <div class="col-md-6">
                <small class="text-muted">HR Name</small>
                <p class="mb-0">
                  {{ company.hr_name || "Not provided" }}
                </p>
              </div>

              <div class="col-md-6">
                <small class="text-muted">HR Email</small>
                <p class="mb-0">
                  {{ company.hr_email || "Not provided" }}
                </p>
              </div>

              <div class="col-md-6">
                <small class="text-muted">HR Contact</small>
                <p class="mb-0">
                  {{ company.hr_contact || "Not provided" }}
                </p>
              </div>

              <div class="col-md-6">
                <small class="text-muted">Website</small>
                <p class="mb-0">
                  <a
                    v-if="company.website"
                    :href="company.website"
                    target="_blank"
                  >
                    {{ company.website }}
                  </a>

                  <span v-else>
                    Not provided
                  </span>
                </p>
              </div>

            </div>

          </div>

          <div class="modal-footer">

            <button
              class="btn btn-outline-primary"
              @click="viewDrives"
            >
              View Company Drives
            </button>

            
            <button
              class="btn btn-outline-secondary"
              @click="closeModal"
            >
              Close
            </button>

            <button
              v-if="company.status !== 'Approved'"
              class="btn btn-success"
              @click="approveCompany"
            >
              Approve Company
            </button>

            <button
              v-if="company.status !== 'Rejected'"
              class="btn btn-danger"
              @click="rejectCompany"
            >
              Reject Company
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
  company: {
    type: Object,
    required: true
  }
})

const emit = defineEmits([
  "close",
  "approve",
  "reject",
  "view-drives"
])


function viewDrives() {
  emit("view-drives", props.company)
}

const statusClass = computed(() => {
  if (props.company.status === "Approved") {
    return "bg-success"
  }

  if (props.company.status === "Rejected") {
    return "bg-danger"
  }

  if (props.company.status === "Blacklisted") {
    return "bg-dark"
  }

  return "bg-warning text-dark"
})

function closeModal() {
  emit("close")
}

function approveCompany() {
  emit("approve", props.company.id)
}

function rejectCompany() {
  emit("reject", props.company.id)
}
</script>
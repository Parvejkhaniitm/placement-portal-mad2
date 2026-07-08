<template>
  <div>
    <div class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">

          <div class="modal-header">
            <h5 class="modal-title">
              Student Details
            </h5>

            <button
              type="button"
              class="btn-close"
              @click="closeModal"
            ></button>
          </div>

          <div class="modal-body">

            <h4 class="mb-1">
              {{ student.name }}
            </h4>

            <span
              class="badge"
              :class="statusClass"
            >
              {{ student.status }}
            </span>

            <hr>

            <div class="row g-3">

              <div class="col-md-6">
                <small class="text-muted">Student ID</small>
                <p class="mb-0">
                  {{ student.id }}
                </p>
              </div>

              <div class="col-md-6">
                <small class="text-muted">Email</small>
                <p class="mb-0">
                  {{ student.email || "Not provided" }}
                </p>
              </div>

              <div class="col-md-6">
                <small class="text-muted">Branch</small>
                <p class="mb-0">
                  {{ student.branch || "Not provided" }}
                </p>
              </div>

              <div class="col-md-6">
                <small class="text-muted">Year</small>
                <p class="mb-0">
                  {{ student.year || "Not provided" }}
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
              v-if="student.status !== 'Blacklisted'"
              class="btn btn-danger"
              @click="blacklistStudent"
            >
              Blacklist Student
            </button>

            <button
              v-else
              class="btn btn-success"
              @click="reactivateStudent"
            >
              Reactivate Student
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
  student: {
    type: Object,
    required: true
  }
})

const emit = defineEmits([
  "close",
  "blacklist",
  "reactivate"
])

const statusClass = computed(() => {
  if (props.student.status === "Active") {
    return "bg-success"
  }

  if (props.student.status === "Blacklisted") {
    return "bg-danger"
  }

  return "bg-secondary"
})

function closeModal() {
  emit("close")
}

function blacklistStudent() {
  emit("blacklist", props.student.id)
}

function reactivateStudent() {
  emit("reactivate", props.student.id)
}
</script>
<template>
  <div>
    <div class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content">

          <div class="modal-header">
            <h5 class="modal-title">
              Drives Posted by {{ company.name }}
            </h5>

            <button
              type="button"
              class="btn-close"
              @click="closeModal"
            ></button>
          </div>

          <div class="modal-body">

            <div
              v-if="loading"
              class="text-center py-4"
            >
              <div class="spinner-border text-primary"></div>
            </div>

            <div
              v-else-if="drives.length === 0"
              class="alert alert-info mb-0"
            >
              This company has not posted any drive yet.
            </div>

            <div
              v-else
              class="table-responsive"
            >
              <table class="table table-hover align-middle">

                <thead class="table-light">
                  <tr>
                    <th>Drive</th>
                    <th>Branches</th>
                    <th>Year</th>
                    <th>Deadline</th>
                    <th>Status</th>
                    <th>Applicants</th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="drive in drives"
                    :key="drive.id"
                  >
                    <td>
                      <strong>{{ drive.title }}</strong>
                      <p class="text-muted small mb-0">
                        {{ drive.description }}
                      </p>
                    </td>

                    <td>
                      {{ drive.branches.join(", ") }}
                    </td>

                    <td>
                      {{ drive.year === 0 ? "Any Year" : drive.year }}
                    </td>

                    <td>
                      {{ formatDate(drive.deadline_date) }}
                    </td>

                    <td>
                      <span
                        class="badge"
                        :class="getStatusClass(drive.status)"
                      >
                        {{ drive.status }}
                      </span>
                    </td>

                    <td>
                      <span class="badge bg-primary">
                        {{ drive.applicant_count }}
                      </span>
                    </td>
                  </tr>
                </tbody>

              </table>
            </div>

          </div>

          <div class="modal-footer">
            <button
              class="btn btn-outline-secondary"
              @click="closeModal"
            >
              Close
            </button>
          </div>

        </div>
      </div>
    </div>

    <div class="modal-backdrop fade show"></div>
  </div>
</template>

<script setup>
defineProps({
  company: {
    type: Object,
    required: true
  },

  drives: {
    type: Array,
    required: true
  },

  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  "close"
])

function closeModal() {
  emit("close")
}

function getStatusClass(status) {
  if (status === "Approved") {
    return "bg-success"
  }

  if (status === "Rejected") {
    return "bg-danger"
  }

  if (status === "Pending") {
    return "bg-warning text-dark"
  }

  return "bg-secondary"
}

function formatDate(dateValue) {
  if (!dateValue) {
    return "-"
  }

  return new Date(dateValue).toLocaleDateString()
}
</script>
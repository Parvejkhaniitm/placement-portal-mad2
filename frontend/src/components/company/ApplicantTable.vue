<template>
  <section class="card border-0 shadow-sm mt-4">

    <div class="card-body p-4">

      <!-- HEADING -->
      <div class="d-flex justify-content-between align-items-center mb-3">

        <h5 class="mb-0">
          Applicants —
          <span class="text-primary">
            {{ drive.title }}
          </span>
        </h5>

        <button
          class="btn-close"
          @click="closeTable"
        ></button>

      </div>

      <!-- LOADING -->
      <div
        v-if="loading"
        class="text-center py-4"
      >
        <div class="spinner-border text-primary"></div>

        <p class="text-muted mt-2">
          Loading applicants...
        </p>
      </div>

      <!-- NO APPLICANTS -->
      <div
        v-else-if="applicants.length === 0"
        class="alert alert-info mb-0"
      >
        No student has applied for this drive.
      </div>

      <!-- APPLICANTS TABLE -->
      <div
        v-else
        class="table-responsive"
      >
        <table class="table table-hover align-middle">

          <thead class="table-light">
            <tr>
              <th>Student ID</th>
              <th>Name</th>
              <th>Branch</th>
              <th>Year</th>
              <th>Applied Date</th>
              <th>Status</th>
              <th>Update Status</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="applicant in applicants"
              :key="applicant.application_id"
            >
              <td>
                {{ applicant.student_id }}
              </td>

              <td>
                <strong>{{ applicant.name }}</strong>
                <br>

                <small class="text-muted">
                  {{ applicant.email }}
                </small>
              </td>

              <td>{{ applicant.branch }}</td>

              <td>{{ applicant.year }}</td>

              <td>
                {{ formatDate(applicant.applied_date) }}
              </td>

              <td>
                <span
                  class="badge"
                  :class="getStatusClass(applicant.status)"
                >
                  {{ applicant.status }}
                </span>
              </td>

              <td>
                <select
                  class="form-select form-select-sm"
                  :value="applicant.status"
                  @change="changeStatus(
                    applicant,
                    $event.target.value
                  )"
                >
                  <option value="Applied">
                    Applied
                  </option>

                  <option value="Shortlisted">
                    Shortlisted
                  </option>

                  <option value="Selected">
                    Selected
                  </option>

                  <option value="Rejected">
                    Rejected
                  </option>
                </select>
              </td>

            </tr>

          </tbody>

        </table>
      </div>

    </div>

  </section>
</template>

<script setup>
defineProps({
  drive: {
    type: Object,
    required: true
  },

  applicants: {
    type: Array,
    required: true
  },

  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  "change-status",
  "close"
])

function changeStatus(applicant, newStatus) {
  emit("change-status", {
    applicant,
    newStatus
  })
}

function closeTable() {
  emit("close")
}

function getStatusClass(status) {
  if (status === "Selected") {
    return "bg-success"
  }

  if (status === "Shortlisted") {
    return "bg-warning text-dark"
  }

  if (status === "Rejected") {
    return "bg-danger"
  }

  return "bg-primary"
}

function formatDate(dateValue) {
  if (!dateValue) {
    return "-"
  }

  return new Date(dateValue).toLocaleDateString()
}
</script>
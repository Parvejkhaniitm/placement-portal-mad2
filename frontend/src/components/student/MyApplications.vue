<template>
  <div class="card border-0 shadow-sm">

    <div class="card-body p-4">

      <h4 class="mb-3">
        My Applications
      </h4>

      <div
        v-if="applications.length === 0"
        class="alert alert-info mb-0"
      >
        You have not applied to any placement drive yet.
      </div>

      <div
        v-else
        class="table-responsive"
      >
        <table class="table table-hover align-middle">

          <thead class="table-light">
            <tr>
              <th>Drive</th>
              <th>Company</th>
              <th>Applied On</th>
              <th>Deadline</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="application in applications"
              :key="application.application_id"
            >
              <td>
                {{ application.drive_title }}
              </td>

              <td>
                {{ application.company_name }}
              </td>

              <td>
                {{ formatDate(application.applied_date) }}
              </td>

              <td>
                {{ formatDate(application.deadline_date) }}
              </td>

              <td>
                <span
                  class="badge"
                  :class="getStatusClass(application.status)"
                >
                  {{ application.status }}
                </span>
              </td>
            </tr>
          </tbody>

        </table>
      </div>

    </div>

  </div>
</template>

<script setup>
defineProps({
  applications: {
    type: Array,
    required: true
  }
})

function getStatusClass(status) {
  if (status === "Applied") {
    return "bg-primary"
  }

  if (status === "Shortlisted") {
    return "bg-warning text-dark"
  }

  if (status === "Selected") {
    return "bg-success"
  }

  if (status === "Rejected") {
    return "bg-danger"
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
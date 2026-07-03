<template>
  <div class="card border-0 shadow-sm">

    <div class="card-body p-4">

      <h4 class="mb-3">
        Company Management
      </h4>

      <!-- LOADING -->
      <div
        v-if="loading"
        class="text-center py-4"
      >
        <div class="spinner-border text-primary"></div>
      </div>

      <!-- NO COMPANIES -->
      <div
        v-else-if="companies.length === 0"
        class="alert alert-info mb-0"
      >
        No registered companies found.
      </div>

      <!-- COMPANY TABLE -->
      <div
        v-else
        class="table-responsive"
      >

        <table class="table table-hover align-middle">

          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Company</th>
              <th>HR Email</th>
              <th>Contact</th>
              <th>Website</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="company in companies"
              :key="company.id"
            >

              <td>{{ company.id }}</td>

              <td>{{ company.name }}</td>

              <td>{{ company.hr_email }}</td>

              <td>{{ company.hr_contact }}</td>

              <td>
                <a
                  :href="company.website"
                  target="_blank"
                >
                  {{ company.website }}
                </a>
              </td>

              <td>
                <span
                  class="badge"
                  :class="getStatusClass(company.status)"
                >
                  {{ company.status }}
                </span>
              </td>

              <td>
                <button
                  v-if="company.status === 'Approved'"
                  class="btn btn-outline-danger btn-sm"
                  @click="blacklistCompany(company.id)"
                >
                  Blacklist
                </button>

                <button
                  v-else-if="company.status === 'Blacklisted'"
                  class="btn btn-outline-success btn-sm"
                  @click="reactivateCompany(company.id)"
                >
                  Reactivate
                </button>

                <span
                  v-else
                  class="text-muted small"
                >
                  Manage from Pending Approvals
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
  companies: {
    type: Array,
    required: true
  },

  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  "blacklist",
  "reactivate"
])

function blacklistCompany(companyId) {
  emit("blacklist", companyId)
}

function reactivateCompany(companyId) {
  emit("reactivate", companyId)
}

function getStatusClass(status) {
  if (status === "Approved") {
    return "bg-success"
  }

  if (status === "Pending") {
    return "bg-warning text-dark"
  }

  return "bg-danger"
}
</script>
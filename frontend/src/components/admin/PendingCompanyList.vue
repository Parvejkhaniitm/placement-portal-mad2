<template>
  <div class="card border-0 shadow-sm">

    <div class="card-body p-4">

      <h4 class="mb-3">
        Pending Company Approvals
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
        No company is waiting for approval.
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
              <th>Website</th>
              <th>Status</th>
              <th>Actions</th>
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

              <td>
                <a
                  :href="company.website"
                  target="_blank"
                >
                  {{ company.website }}
                </a>
              </td>

              <td>
                <span class="badge bg-warning text-dark">
                  {{ company.status }}
                </span>
              </td>

              <td>

                <button
                class="btn btn-outline-secondary btn-sm me-2"
                @click="viewCompany(company)"
                >
                  View
                </button>
                
                <button
                  class="btn btn-success btn-sm me-2"
                  @click="approveCompany(company.id)"
                >
                  Approve
                </button>

                <button
                  class="btn btn-danger btn-sm"
                  @click="rejectCompany(company.id)"
                >
                  Reject
                </button>
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
  "view",
  "approve",
  "reject"
])

function approveCompany(companyId) {
  emit("approve", companyId)
}

function rejectCompany(companyId) {
  emit("reject", companyId)
}

function viewCompany(company) {
  emit("view", company)
}
</script>
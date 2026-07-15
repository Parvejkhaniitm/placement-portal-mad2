<template>
  <div class="card border-0 shadow-sm">

    <div class="card-body p-4">

      <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-4">
        <div>
          <h4 class="mb-1">
            Reports & Stats
          </h4>

          <p class="text-muted mb-0">
            Quick overview of the placement portal.
          </p>
        </div>

        <span class="badge bg-info-subtle text-info">
          Summary
        </span>
      </div>

      <div class="row g-3">

        <div class="col-12 col-md-4">
          <div class="border rounded p-3 h-100 bg-light">
            <p class="text-muted mb-1">
              Total Students
            </p>

            <h3 class="mb-0">
              {{ stats.total_students }}
            </h3>
          </div>
        </div>

        <div class="col-12 col-md-4">
          <div class="border rounded p-3 h-100 bg-light">
            <p class="text-muted mb-1">
              Total Companies
            </p>

            <h3 class="mb-0">
              {{ stats.total_company }}
            </h3>
          </div>
        </div>

        <div class="col-12 col-md-4">
          <div class="border rounded p-3 h-100 bg-light">
            <p class="text-muted mb-1">
              Total Drives
            </p>

            <h3 class="mb-0">
              {{ stats.total_drive }}
            </h3>
          </div>
        </div>

      </div>

      <div class="alert alert-info mt-4 mb-0">
        Reports can later include selected students, rejected applications,
        company-wise drives, and branch-wise placement data.
      </div>

    </div>

  </div>
</template>

<script setup>
defineProps({
  stats: {
    type: Object,
    required: true
  }
})
</script>
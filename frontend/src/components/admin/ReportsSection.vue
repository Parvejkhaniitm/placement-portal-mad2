<template>
  <div class="card border-0 shadow-sm">

    <div class="card-body p-4">

      <h4 class="mb-3">
        Reports & Stats
      </h4>

      <p class="text-muted">
        Quick summary of the placement portal.
      </p>

      <div class="row g-3">

        <div class="col-12 col-md-4">
          <div class="border rounded p-3 h-100">
            <p class="text-muted mb-1">
              Students
            </p>

            <h3 class="mb-0">
              {{ stats.total_students }}
            </h3>
          </div>
        </div>

        <div class="col-12 col-md-4">
          <div class="border rounded p-3 h-100">
            <p class="text-muted mb-1">
              Companies
            </p>

            <h3 class="mb-0">
              {{ stats.total_company }}
            </h3>
          </div>
        </div>

        <div class="col-12 col-md-4">
          <div class="border rounded p-3 h-100">
            <p class="text-muted mb-1">
              Placement Drives
            </p>

            <h3 class="mb-0">
              {{ stats.total_drive }}
            </h3>
          </div>
        </div>

      </div>

      <hr class="my-4">

      <div class="alert alert-info mb-0">
        More detailed reports can be added later, like selected students,
        rejected applications, company-wise drives, and branch-wise placement data.
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
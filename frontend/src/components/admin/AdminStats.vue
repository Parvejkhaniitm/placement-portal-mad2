<template>
  <div class="row g-3 mb-4">

    <div class="col-12 col-md-4">
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body p-4">

          <div class="d-flex justify-content-between align-items-center">

            <div>
              <p class="text-muted mb-1">
                Registered Students
              </p>

              <h2 class="mb-0">
                {{ stats.total_students }}
              </h2>
            </div>

            <span class="badge bg-primary-subtle text-primary">
              Students
            </span>

          </div>

        </div>
      </div>
    </div>

    <div class="col-12 col-md-4">
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body p-4">

          <div class="d-flex justify-content-between align-items-center">

            <div>
              <p class="text-muted mb-1">
                Registered Companies
              </p>

              <h2 class="mb-0">
                {{ stats.total_company }}
              </h2>
            </div>

            <span class="badge bg-success-subtle text-success">
              Companies
            </span>

          </div>

        </div>
      </div>
    </div>

    <div class="col-12 col-md-4">
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body p-4">

          <div class="d-flex justify-content-between align-items-center">

            <div>
              <p class="text-muted mb-1">
                Placement Drives
              </p>

              <h2 class="mb-0">
                {{ stats.total_drive }}
              </h2>
            </div>

            <span class="badge bg-warning-subtle text-warning">
              Drives
            </span>

          </div>

        </div>
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
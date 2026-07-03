<template>
  <div class="row g-3 mb-4">

    <!-- STUDENTS -->
    <div class="col-12 col-md-4">

      <div class="card border-0 shadow-sm h-100">

        <div class="card-body p-4">

          <p class="text-muted mb-2">
            Registered Students
          </p>

          <h2 class="mb-0">
            {{ stats.total_students }}
          </h2>

        </div>

      </div>

    </div>

    <!-- COMPANIES -->
    <div class="col-12 col-md-4">

      <div class="card border-0 shadow-sm h-100">

        <div class="card-body p-4">

          <p class="text-muted mb-2">
            Registered Companies
          </p>

          <h2 class="mb-0">
            {{ stats.total_company }}
          </h2>

        </div>

      </div>

    </div>

    <!-- DRIVES -->
    <div class="col-12 col-md-4">

      <div class="card border-0 shadow-sm h-100">

        <div class="card-body p-4">

          <p class="text-muted mb-2">
            Placement Drives
          </p>

          <h2 class="mb-0">
            {{ stats.total_drive }}
          </h2>

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
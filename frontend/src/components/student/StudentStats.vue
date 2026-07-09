<template>
  <div class="row g-3 mb-4">

    <div class="col-12 col-md-4">
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body">
          <p class="text-muted mb-1">
            Active Drives
          </p>

          <h3>
            {{ statistics.active_drives }}
          </h3>
        </div>
      </div>
    </div>

    <div class="col-12 col-md-4">
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body">
          <p class="text-muted mb-1">
            Applications
          </p>

          <h3>
            {{ statistics.total_applications }}
          </h3>
        </div>
      </div>
    </div>

    <div class="col-12 col-md-4">
      <div class="card border-0 shadow-sm h-100">
        <div class="card-body">
          <p class="text-muted mb-1">
            Selected
          </p>

          <h3>
            {{ statistics.selected_applications }}
          </h3>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
defineProps({
  statistics: {
    type: Object,
    required: true
  }
})
</script>
<template>
  <div class="card border-0 shadow-sm h-100">

    <div class="card-body p-4">

      <h5>Create Placement Drive</h5>

      <p class="text-muted">
        Post a new opportunity for eligible students.
      </p>

      <button
        class="btn btn-primary w-100 py-2"
        :disabled="!canCreateDrive"
        @click="createDrive"
      >
        + Create New Drive
      </button>

      <div
        v-if="!canCreateDrive"
        class="alert alert-warning mt-3 mb-0"
      >
        Admin approval is required to create a drive.
      </div>

      <hr class="my-4">

      <div class="row text-center">

        <div class="col-4 border-end">
          <h3 class="mb-1">
            {{ statistics.active_drives }}
          </h3>

          <small class="text-muted">
            Active Drives
          </small>
        </div>

        <div class="col-4 border-end">
          <h3 class="mb-1">
            {{ statistics.total_drives }}
          </h3>

          <small class="text-muted">
            Total Drives
          </small>
        </div>

        <div class="col-4">
          <h3 class="mb-1">
            {{ statistics.total_applicants }}
          </h3>

          <small class="text-muted">
            Applicants
          </small>
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
  },

  canCreateDrive: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(["create-drive"])

function createDrive() {
  emit("create-drive")
}
</script>
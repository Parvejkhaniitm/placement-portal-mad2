<template>
  <section class="mt-4">

    <h4 class="mb-3">
      Placement Drives
    </h4>

    <!-- NO DRIVES -->
    <div
      v-if="drives.length === 0"
      class="alert alert-info"
    >
      You have not created any placement drive.
    </div>

    <!-- DRIVE CARDS -->
    <div
      v-else
      class="row g-3"
    >

      <div
        v-for="drive in drives"
        :key="drive.id"
        class="col-12 col-md-6 col-xl-4"
      >

        <DriveCard
          :drive="drive"
          @manage-applicants="manageApplicants"
        />

      </div>

    </div>

  </section>
</template>

<script setup>
import DriveCard from
  "@/components/company/DriveCard.vue"

defineProps({
  drives: {
    type: Array,
    required: true
  }
})

const emit = defineEmits([
  "manage-applicants"
])

function manageApplicants(drive) {
  emit("manage-applicants", drive)
}
</script>
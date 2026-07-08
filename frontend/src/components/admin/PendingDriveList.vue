<template>
  <div class="card border-0 shadow-sm mt-4">

    <div class="card-body p-4">

      <h4 class="mb-3">
        Pending Placement Drives
      </h4>

      <!-- NO PENDING DRIVES -->
      <div
        v-if="drives.length === 0"
        class="alert alert-info mb-0"
      >
        No placement drive is waiting for approval.
      </div>

      <!-- DRIVE TABLE -->
      <div
        v-else
        class="table-responsive"
      >

        <table class="table table-hover align-middle">

          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Drive</th>
              <th>Company</th>
              <th>Branches</th>
              <th>Year</th>
              <th>Deadline</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="drive in drives"
              :key="drive.id"
            >

              <td>{{ drive.id }}</td>

              <td>{{ drive.title }}</td>

              <td>{{ drive.company_name }}</td>

              <td>
                {{ drive.branches.join(", ") }}
              </td>

              <td>{{ drive.year }}</td>

              <td>
                {{ formatDate(drive.deadline_date) }}
              </td>

              <td>
                <span class="badge bg-warning text-dark">
                  {{ drive.status }}
                </span>
              </td>

              <td>

                <button
                 class="btn btn-outline-secondary btn-sm me-2"
                 @click="viewDrive(drive)"
                >
                View
                </button>

                <button
                  class="btn btn-success btn-sm me-2"
                  @click="approveDrive(drive.id)"
                >
                  Approve
                </button>

                <button
                  class="btn btn-danger btn-sm"
                  @click="rejectDrive(drive.id)"
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
  drives: {
    type: Array,
    required: true
  }
})

const emit = defineEmits([
  "view",
  "approve",
  "reject"
])

function viewDrive(drive) {
  emit("view", drive)
}

function approveDrive(driveId) {
  emit("approve", driveId)
}

function rejectDrive(driveId) {
  emit("reject", driveId)
}

function formatDate(dateValue) {
  if (!dateValue) {
    return "-"
  }

  return new Date(dateValue).toLocaleDateString()
}
</script>
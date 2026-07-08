<template>
  <div class="card border-0 shadow-sm">

    <div class="card-body p-4">

      <h4 class="mb-3">
        Student Management
      </h4>

      <!-- LOADING -->
      <div
        v-if="loading"
        class="text-center py-4"
      >
        <div class="spinner-border text-primary"></div>
      </div>

      <!-- NO STUDENTS -->
      <div
        v-else-if="students.length === 0"
        class="alert alert-info mb-0"
      >
        No registered students found.
      </div>

      <!-- STUDENT TABLE -->
      <div
        v-else
        class="table-responsive"
      >

        <table class="table table-hover align-middle">

          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Branch</th>
              <th>Year</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="student in students"
              :key="student.id"
            >

              <td>{{ student.id }}</td>

              <td>{{ student.name }}</td>

              <td>{{ student.branch }}</td>

              <td>{{ student.year }}</td>

              <td>
                <span
                  class="badge"
                  :class="student.status === 'Active'
                    ? 'bg-success'
                    : 'bg-danger'"
                >
                  {{ student.status }}
                </span>
              </td>

<td>
  <button
    class="btn btn-outline-secondary btn-sm me-2"
    @click="viewStudent(student)"
  >
    View
  </button>

  <button
    v-if="student.status === 'Active'"
    class="btn btn-outline-danger btn-sm"
    @click="blacklistStudent(student.id)"
  >
    Blacklist
  </button>

  <button
    v-else
    class="btn btn-outline-success btn-sm"
    @click="reactivateStudent(student.id)"
  >
    Reactivate
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
  students: {
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
  "blacklist",
  "reactivate"
])

function blacklistStudent(studentId) {
  emit("blacklist", studentId)
}

function reactivateStudent(studentId) {
  emit("reactivate", studentId)
}

function viewStudent(student) {
  emit("view", student)
}
</script>
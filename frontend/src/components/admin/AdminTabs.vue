<template>
  <div class="card border-0 shadow-sm mb-4">

    <div class="card-body pb-0">

      <ul class="nav nav-tabs">

        <!-- PENDING APPROVALS -->
        <li class="nav-item">

          <button
            class="nav-link"
            :class="{ active: activeSection === 'pending' }"
            @click="changeSection('pending')"
          >
            Pending Approvals

            <span class="badge bg-warning text-dark ms-1">
              {{ pendingCount }}
            </span>
          </button>

        </li>

        <!-- STUDENTS -->
        <li class="nav-item">

          <button
            class="nav-link"
            :class="{ active: activeSection === 'students' }"
            @click="changeSection('students')"
          >
            Students
          </button>

        </li>

        <!-- COMPANIES -->
        <li class="nav-item">

          <button
            class="nav-link"
            :class="{ active: activeSection === 'companies' }"
            @click="changeSection('companies')"
          >
            Companies
          </button>

        </li>

        <!-- REPORTS -->
        <li class="nav-item">

          <button
            class="nav-link"
            :class="{ active: activeSection === 'reports' }"
            @click="changeSection('reports')"
          >
            Reports
          </button>

        </li>

      </ul>

    </div>

  </div>
</template>

<script setup>
defineProps({
  activeSection: {
    type: String,
    required: true
  },

  pendingCount: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits([
  "change-section"
])

function changeSection(sectionName) {
  emit("change-section", sectionName)
}
</script>
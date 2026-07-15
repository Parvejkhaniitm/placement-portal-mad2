<template>
  <div class="card border-0 shadow-sm mt-4">

    <div class="card-body p-4">

      <div class="d-flex justify-content-between mb-4">
        <div>
          <h5 class="mb-1">Create Placement Drive</h5>

          <p class="text-muted mb-0">
            Enter the placement opportunity details.
          </p>
        </div>

        <button
          type="button"
          class="btn-close"
          @click="cancelForm"
        ></button>
      </div>

      <form @submit.prevent="submitForm">

        <!-- TITLE -->
        <div class="mb-3">
          <label class="form-label">
            Drive Title
          </label>

          <input
            v-model.trim="driveForm.title"
            type="text"
            class="form-control"
            placeholder="Example: Backend Developer"
            required
          >
        </div>

        <!-- DESCRIPTION -->
        <div class="mb-3">
          <label class="form-label">
            Description
          </label>

          <textarea
            v-model.trim="driveForm.description"
            class="form-control"
            rows="3"
            placeholder="Enter job description"
            required
          ></textarea>
        </div>

        <!-- BRANCHES -->
        <div class="mb-3">
          <label class="form-label d-block">
            Eligible Branches
          </label>

          <div class="form-check form-check-inline">
            <input
              id="cse"
              v-model="driveForm.branches"
              class="form-check-input"
              type="checkbox"
              value="CSE"
            >

            <label
              class="form-check-label"
              for="cse"
            >
              CSE
            </label>
          </div>

          <div class="form-check form-check-inline">
            <input
              id="it"
              v-model="driveForm.branches"
              class="form-check-input"
              type="checkbox"
              value="IT"
            >

            <label
              class="form-check-label"
              for="it"
            >
              IT
            </label>
          </div>

          <div class="form-check form-check-inline">
            <input
              id="ece"
              v-model="driveForm.branches"
              class="form-check-input"
              type="checkbox"
              value="ECE"
            >

            <label
              class="form-check-label"
              for="ece"
            >
              ECE
            </label>
          </div>

          <div class="form-check form-check-inline">
            <input
              id="mechanical"
              v-model="driveForm.branches"
              class="form-check-input"
              type="checkbox"
              value="Mechanical"
            >

            <label
              class="form-check-label"
              for="mechanical"
            >
              Mechanical
            </label>
          </div>

          <p
            v-if="branchError"
            class="text-danger small mt-2"
          >
            Please select at least one branch.
          </p>
        </div>

        <div class="row">

          <!-- YEAR -->
          <div class="col-md-6 mb-3">
            <label class="form-label">
              Eligible Year
            </label>

            <select
              v-model="driveForm.year"
              class="form-select"
              required
            >
              <option disabled value="">
                Select year
              </option>
              <option value="0">Any Year</option>
              <option value="1">1st Year</option>
              <option value="2">2nd Year</option>
              <option value="3">3rd Year</option>
              <option value="4">4th Year</option>
            </select>
          </div>

          <!-- DEADLINE -->
          <div class="col-md-6 mb-3">
            <label class="form-label">
              Application Deadline
            </label>

            <input
              v-model="driveForm.deadline_date"
              type="date"
              class="form-control"
              required
            >
          </div>

        </div>

        <!-- BUTTONS -->
        <div class="d-flex gap-2">

          <button
            type="submit"
            class="btn btn-primary"
            :disabled="creating"
          >
            {{ creating ? "Creating..." : "Create Drive" }}
          </button>

          <button
            type="button"
            class="btn btn-outline-secondary"
            :disabled="creating"
            @click="cancelForm"
          >
            Cancel
          </button>

        </div>

      </form>

    </div>

  </div>
</template>

<script setup>
import { reactive, ref } from "vue"

defineProps({
  creating: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  "submit",
  "cancel"
])

const branchError = ref(false)

const driveForm = reactive({
  title: "",
  description: "",
  branches: [],
  year: "",
  deadline_date: ""
})

function submitForm() {
  if (driveForm.branches.length === 0) {
    branchError.value = true
    return
  }

  branchError.value = false

  emit("submit", {
    title: driveForm.title,
    description: driveForm.description,
    branches: [...driveForm.branches],
    year: Number(driveForm.year),
    deadline_date: driveForm.deadline_date
  })
}

function cancelForm() {
  emit("cancel")
}
</script>
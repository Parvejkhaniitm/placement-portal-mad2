<template>
  <div class="card border-0 shadow-sm mb-4">

    <div class="card-body p-4">

      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="mb-0">
          Edit Profile
        </h4>

        <button
          type="button"
          class="btn-close"
          @click="cancelForm"
        ></button>
      </div>

      <form @submit.prevent="submitForm">

        <div class="mb-3">
          <label class="form-label">
            Full Name
          </label>

          <input
            v-model.trim="profileForm.name"
            type="text"
            class="form-control"
            required
          >
        </div>

        <div class="mb-3">
          <label class="form-label">
            Branch
          </label>

          <select
            v-model="profileForm.branch"
            class="form-select"
            required
          >
            <option disabled value="">
              Select branch
            </option>

            <option value="CSE">CSE</option>
            <option value="IT">IT</option>
            <option value="ECE">ECE</option>
            <option value="Mechanical">Mechanical</option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label">
            Year
          </label>

          <select
            v-model="profileForm.year"
            class="form-select"
            required
          >
            <option disabled value="">
              Select year
            </option>

            <option value="1">1st Year</option>
            <option value="2">2nd Year</option>
            <option value="3">3rd Year</option>
            <option value="4">4th Year</option>
          </select>
        </div>

        <div class="d-flex gap-2">

          <button
            type="submit"
            class="btn btn-primary"
            :disabled="saving"
          >
            {{ saving ? "Saving..." : "Save Profile" }}
          </button>

          <button
            type="button"
            class="btn btn-outline-secondary"
            :disabled="saving"
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
import { reactive, watch } from "vue"

const props = defineProps({
  student: {
    type: Object,
    required: true
  },

  saving: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  "save",
  "cancel"
])

const profileForm = reactive({
  name: "",
  branch: "",
  year: ""
})

watch(
  () => props.student,
  (student) => {
    profileForm.name = student.name || ""
    profileForm.branch = student.branch || ""
    profileForm.year = student.year
      ? String(student.year)
      : ""
  },
  {
    immediate: true
  }
)

function submitForm() {
  emit("save", {
    name: profileForm.name,
    branch: profileForm.branch,
    year: Number(profileForm.year)
  })
}

function cancelForm() {
  emit("cancel")
}
</script>
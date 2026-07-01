<template>
  <div class="card border-0 shadow-sm h-100">

    <div class="card-body p-4">

      <!-- HEADING -->
      <div class="d-flex justify-content-between align-items-center mb-4">

        <h5 class="mb-0">
          Company Profile
        </h5>

        <button
          v-if="!editing"
          class="btn btn-outline-primary btn-sm"
          @click="startEditing"
        >
          Edit
        </button>

      </div>

      <!-- PROFILE DETAILS -->
      <div v-if="!editing">

        <p class="text-secondary small mb-1">
          Company Name
        </p>

        <p class="bg-light border rounded p-2">
          {{ company.name }}
        </p>

        <p class="text-secondary small mb-1">
          HR Name
        </p>

        <p class="bg-light border rounded p-2">
          {{ company.hr_name }}
        </p>

        <p class="text-secondary small mb-1">
          HR Email
        </p>

        <p class="bg-light border rounded p-2">
          {{ company.hr_email }}
        </p>

        <p class="text-secondary small mb-1">
          HR Contact
        </p>

        <p class="bg-light border rounded p-2">
          {{ company.hr_contact }}
        </p>

        <p class="text-secondary small mb-1">
          Website
        </p>

        <p class="bg-light border rounded p-2 mb-0">
          {{ company.website }}
        </p>

      </div>

      <!-- EDIT PROFILE FORM -->
      <form
        v-else
        @submit.prevent="saveProfile"
      >

        <div class="mb-3">
          <label class="form-label">
            Company Name
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
            HR Name
          </label>

          <input
            v-model.trim="profileForm.hr_name"
            type="text"
            class="form-control"
            required
          >
        </div>

        <div class="mb-3">
          <label class="form-label">
            HR Email
          </label>

          <input
            v-model.trim="profileForm.hr_email"
            type="email"
            class="form-control"
            required
          >
        </div>

        <div class="mb-3">
          <label class="form-label">
            HR Contact
          </label>

          <input
            v-model.trim="profileForm.hr_contact"
            type="text"
            class="form-control"
            required
          >
        </div>

        <div class="mb-4">
          <label class="form-label">
            Website
          </label>

          <input
            v-model.trim="profileForm.website"
            type="url"
            class="form-control"
            placeholder="https://example.com"
            required
          >
        </div>

        <div class="d-flex gap-2">

          <button
            type="submit"
            class="btn btn-primary"
            :disabled="saving"
          >
            {{ saving ? "Saving..." : "Save Changes" }}
          </button>

          <button
            type="button"
            class="btn btn-outline-secondary"
            :disabled="saving"
            @click="cancelEditing"
          >
            Cancel
          </button>

        </div>

      </form>

    </div>

  </div>
</template>

<script setup>
import { reactive, ref, watch } from "vue"

const props = defineProps({
  company: {
    type: Object,
    required: true
  },

  saving: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(["save"])

const editing = ref(false)

const profileForm = reactive({
  name: "",
  hr_name: "",
  hr_email: "",
  hr_contact: "",
  website: ""
})

function copyCompanyToForm() {
  profileForm.name = props.company.name || ""
  profileForm.hr_name = props.company.hr_name || ""
  profileForm.hr_email = props.company.hr_email || ""
  profileForm.hr_contact = props.company.hr_contact || ""
  profileForm.website = props.company.website || ""
}

function startEditing() {
  copyCompanyToForm()
  editing.value = true
}

function cancelEditing() {
  copyCompanyToForm()
  editing.value = false
}

function saveProfile() {
  emit("save", {
    name: profileForm.name,
    hr_name: profileForm.hr_name,
    hr_email: profileForm.hr_email,
    hr_contact: profileForm.hr_contact,
    website: profileForm.website
  })
}

watch(
  () => props.company,
  () => {
    copyCompanyToForm()

    if (!props.saving) {
      editing.value = false
    }
  },
  {
    deep: true,
    immediate: true
  }
)
</script>
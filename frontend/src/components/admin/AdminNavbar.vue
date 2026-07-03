<template>
  <nav class="navbar bg-white border-bottom px-4 py-3">

    <div class="d-flex align-items-center">

      <div
        class="bg-primary-subtle text-primary rounded-circle
               d-flex justify-content-center align-items-center
               me-3 p-3"
      >
        A
      </div>

      <div>
        <h4 class="mb-1">
          Placement Portal
        </h4>

        <span class="badge bg-primary">
          Administrator
        </span>
      </div>

    </div>

    <button
      class="btn btn-outline-danger"
      @click="logout"
    >
      Logout
    </button>

  </nav>
</template>

<script setup>
const emit = defineEmits(["logout"])

function logout() {
  emit("logout")
}
</script>
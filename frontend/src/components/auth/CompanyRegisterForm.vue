<template>
    <form @submit.prevent="registerCompany">
        <div class="mb-3">
            <label class="form-label fw-semibold small">Company Name</label>
            <input type="text" class="form-control" v-model.trim="name" placeholder="Fill Company Name" required>
        </div>

        <div class="mb-3">
            <label class="form-label fw-semibold small">HR Name</label>
            <input type="text" class="form-control" v-model.trim="hrName" placeholder=" Please Fill Name " required>
        </div>

        <div class="mb-3">
            <label class="form-label">HR Email</label>
            <input type="email" v-model.trim="hrEmail" class="form-control" required>
        </div>

        <div class="mb-3">
            <label class="form-label">Phone Number</label>
            <input type="tel" v-model.trim="phone" class="form-control" required>
        </div>

        <div class="mb-3">
            <label class="form-label">Website</label>
            <input type="url" v-model.trim="website" class="form-control" placeholder="https://example.com" required>
        </div>

        <div class="row">
            <div class="col-md-6 mb-3">
                <label class="form-label">Password</label>
                <input type="password" v-model="password" class="form-control" required>
            </div>
        

            <div class="col-md-6 mb-3">
                <label class="form-label">Confirm Password</label>
                <input type="password" v-model="confirmPassword" class="form-control" required>
            </div>
        </div>

        <div v-if="errorMessages" class="alert alert-danger">
            {{ errorMessages }}
        </div>

        <button type="submit" class="btn btn-primary w-100" >
            submit
        </button>

    </form>
</template>

<script setup>

import { ref } from 'vue';


const emit = defineEmits(["registration-success"])

const name = ref("")
const hrName = ref("")
const hrEmail = ref("")
const phone = ref("")
const website = ref("")
const password = ref("")
const confirmPassword = ref("")
const errorMessages =  ref("")

async function registerCompany() {
    errorMessages.value = ""

    if (password.value !== confirmPassword.value) {
        errorMessages.value = "Passwords do not match"
        return
    }

    const company = {
        name: name.value,
        hr_name: hrName.value,
        hr_email: hrEmail.value,
        phone: phone.value,
        website: website.value,
        password: password.value,
        confirm_password: confirmPassword.value
    }
    const response = await fetch(
        "http://127.0.0.1:5000/api/company_register",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(company)
        }
    )
    const data = await response.json()
    if (!response.ok) {
        errorMessages.value = data.message || "Company registration failed"
        return
    }

    alert(data.message || "Company registered successfully")
    emit("registration-success")

}
</script>
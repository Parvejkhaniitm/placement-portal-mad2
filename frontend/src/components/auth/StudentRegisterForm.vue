<template>
    <form @submit.prevent = "registerStudent">
        <div class="mb-3">
            <label class="form-label fw-semibold small">Full Name</label>
            <input type="text" class="form-control" v-model="name" placeholder="Fill your name...">
        </div>

        <div class="mb-3">
            <label class = "form-label fw-semiboold small">College Email</label>
            <input type="text" class="form-control" v-model="email" placeholder="abc@gmail.com...">
        </div>

        <div class="row">
            <div class="col-6 mb-3">
                <label class="form-label fw-semibold small">Branch</label>
                <select class="form-select" v-model="branch">
                    <option value="">Select Branch</option>
                    <option value="CSE">CSE</option>
                    <option value="IT">IT</option>
                    <option value="ECE">ECE</option>
                    <option value="ME">ME</option>
                    <option value="CE">CE</option>
                </select>
            </div>

            <div class="col-6 mb-3">
                <label  class="form-label fw-semibold small">Graduating Year</label>
                <select class="form-select" v-model="year">
                    <option value="">Select Year</option>
                    <option value="2026">2026</option>
                    <option value="2027">2027</option>
                    <option value="2028">2028</option>
                    <option value="2029">2029</option>
                </select>
            </div>
        </div>

        <div class="row">
            <div class="col-6 mb-3">
                <label class="form-label fw-semibold small">Password</label>
                <input type="password" class="form-control" v-model="password" placeholder="Password">
            </div>

            <div class="col-6 mb-3">
                <label class="form-label fw-semibold small">Confirm Password</label>
                <input type="password" class="form-control" v-model="confirmPassword" placeholder="Confirm Password">
            </div>
        </div>

        <button type="submit" class="btn btn-primary w-100">
            Create Account
        </button>

    </form>
</template>

<script setup>
    import { ref } from 'vue';

    const name = ref('')
    const email = ref('')
    const branch = ref('')
    const year = ref('')
    const password = ref('')
    const confirmPassword = ref('')

    

    async function registerStudent() {
        if ( name.value === '' || email.value === '' || branch.value === '' || password.value === '' || confirmPassword.value === '' || year.value === '') {
            alert('Please fill all the fields')
            return
        }

        if (password.value !== confirmPassword.value) {
            alert("Password and Confirm Password do not match")
            return
        }

        const studentData = {
            name: name.value,
            email: email.value,
            branch: branch.value,
            year: year.value,
            password: password.value,
            confirm_password: confirmPassword.value
        }
        console

        const  response = await fetch (
            'http://127.0.0.1:5000/api/student_register',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(studentData)
            })
        
            const data = await response.json()

            if (!response.ok) {
                alert(`Registration Failed: ${data.message}`)
                return
            }

            alert(data.message)

            name.value = ""
            email.value = ""
            branch.value = ""
            year.value = ""
            password.value = ""
            confirmPassword.value = ""
            
    }



</script>
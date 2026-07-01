<template>
    <div class="container mt-5">
        <div class="card p-4 shadow">

            <h2 class="text-center mb-4">
                Placement Portal Login
            </h2>

            <form v-on:submit.prevent="login">

            <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" v-model="email" @input="validateEmail">
                <div id="emailhelp" class="text-danger" > {{ emailError }}</div>
            </div>

            <div class="mb-3">
                <label class="form-label">Password</label>
                <input type="password" class="form-control" v-model="password">
            </div>

            <button type="submit" class="btn btn-primary w-100" >Login</button>

            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'
const router = useRouter()

const email = ref('')
const password = ref('')


const emailError = ref('')
const validateEmail = () => {

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailPattern.test(email.value)) {
        emailError.value = "Invalid Email";
        return false
        
    } else {
        emailError.value = '';
        return true
    }    
}

 async function login(){
    console.log("login function called")
    if (!validateEmail()) {
        alert("Invalid Email, Please enter valid email")
        return
    } 

    if (email.value === '' || password.value === '') {
        alert("Please fill all the fields")
        return
    }

    const user = {
        email: email.value,
        password: password.value
    }

    const response = await fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(user)
    })


    if (!response.ok) {
        const errorData = await response.json()
        alert(`Login Failed: ${errorData.message}`);
        return
    } else {
        const data = await response.json()
        console.log(data) 

        localStorage.setItem(
            "auth_token",
            data.user_details.auth_token
        )

        localStorage.setItem(
            "role",
            data.user_details.Roles[0]
        )

    const role = data.user_details.Roles[0]

    if (role === "admin") {
        router.push('/admin')
    } else if(role === "Student") {
        router.push('/student')
    } else if (role === 'Company') {
        router.push('/company')
    }

    }
}
</script>
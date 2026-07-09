import {
  createRouter,
  createWebHistory
} from "vue-router"

import LoginView from "@/view/LoginView.vue"
import AdminDashboard from "@/view/AdminDashboard.vue"
import CompanyDashboard from "@/view/CompanyDashboard.vue"
import StudentDashboard from "@/view/StudentDashboard.vue"

const routes = [
  {
    path: "/",
    redirect: "/login"
  },

  {
    path: "/login",
    name: "login",
    component: LoginView
  },

  {
    path: "/admin",
    name: "admin-dashboard",
    component: AdminDashboard,

    meta: {
      requiresAuth: true,
      role: "admin"
    }
  },


  {
    path: "/company",
    name: "company-dashboard",
    component: CompanyDashboard,

    meta: {
      requiresAuth: true,
      role: "Company"
    }
  },

  {
    path: "/student",
    name: "student-dashboard",
    component: StudentDashboard,

    meta: {
      requiresAuth: true,
      role: "Student"
    }
  }


]

const router = createRouter({
  history: createWebHistory(
    import.meta.env.BASE_URL
  ),

  routes
})

router.beforeEach((to) => {
  const token = localStorage.getItem("auth_token")
  const role = localStorage.getItem("role")

  if (to.meta.requiresAuth && !token) {
    return "/login"
  }

  if (
    to.meta.role &&
    role !== to.meta.role
  ) {
    return "/login"
  }

  if (
    to.path === "/login" &&
    token
  ) {
    if (role === "admin") {
      return "/admin"
    }

    if (role === "Company") {
      return "/company"
    }
  }
})

export default router
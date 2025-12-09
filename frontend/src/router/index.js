import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth'

const routes = [
  {
    path: '/',
    name: 'Welcome',
    component: () => import('@/views/Welcome.vue'),
    meta: { requiresAuth: false, title: 'Xush kelibsiz' },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { requiresAuth: false, title: 'Tizimga kirish' },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { requiresAuth: false, title: "Ro'yxatdan o'tish" },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/dashboard/DashboardIndex.vue'),
    meta: { requiresAuth: true, title: 'Dashboard' },
  },
  {
    path: '/students',
    name: 'Students',
    component: () => import('@/views/students/StudentsIndex.vue'),
    meta: { 
      requiresAuth: true, 
      roles: ['SUPERADMIN', 'BOSS', 'ADMIN', 'MENTOR'],
      title: 'Talabalar'
    },
  },
  {
    path: '/students/:id',
    name: 'StudentDetail',
    component: () => import('@/views/students/StudentDetailView.vue'),
    meta: { 
      requiresAuth: true, 
      roles: ['SUPERADMIN', 'BOSS', 'ADMIN', 'MENTOR'],
      title: 'Talaba tafsilotlari'
    },
  },
  {
    path: '/groups',
    name: 'Groups',
    component: () => import('@/views/groups/GroupsIndex.vue'),
    meta: { requiresAuth: true, title: 'Guruhlar' },
  },
  {
    path: '/groups/:id',
    name: 'GroupDetail',
    component: () => import('@/views/groups/GroupDetailView.vue'),
    meta: { requiresAuth: true, title: 'Guruh tafsilotlari' },
  },
  {
    path: '/payments',
    name: 'Payments',
    component: () => import('@/views/payments/PaymentsIndex.vue'),
    meta: { 
      requiresAuth: true, 
      roles: ['SUPERADMIN', 'BOSS', 'ADMIN'],
      title: "To'lovlar" 
    },
  },
  {
    path: '/payouts',
    name: 'Payouts',
    component: () => import('@/views/payouts/PayoutsIndex.vue'),
    meta: { 
      requiresAuth: true, 
      roles: ['SUPERADMIN', 'BOSS', 'ADMIN', 'MENTOR'],
      title: "To'lab berish" 
    },
  },
  {
    path: '/settings/commission',
    name: 'CommissionSettings',
    component: () => import('@/views/settings/CommissionSettings.vue'),
    meta: { 
      requiresAuth: true, 
      roles: ['SUPERADMIN', 'BOSS'],
      title: 'Komissiya sozlamalari'
    },
  },
  {
    path: '/settings/allowlist',
    name: 'AllowlistManagement',
    component: () => import('@/views/settings/AllowlistManagement.vue'),
    meta: { 
      requiresAuth: true, 
      roles: ['SUPERADMIN', 'BOSS'],
      title: 'Email Allowlist'
    },
  },
  {
    path: '/settings/profile',
    name: 'ProfileSettings',
    component: () => import('@/views/settings/ProfileView.vue'),
    meta: { requiresAuth: true, title: 'Profil sozlamalari' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: 'Sahifa topilmadi' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  document.title = `${to.meta.title || 'Training CRM'} - Training CRM`
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.roles && !to.meta.roles.includes(authStore.userRole)) {
    next('/dashboard')
  } else if ((to.name === 'Login' || to.name === 'Register') && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router

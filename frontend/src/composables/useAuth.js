import { computed } from 'vue'
import { useAuthStore } from '@/store/modules/auth'

export function useAuth() {
  const authStore = useAuthStore()

  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const user = computed(() => authStore.user)
  const userRole = computed(() => authStore.userRole)
  
  const isSuperAdmin = computed(() => authStore.isSuperAdmin)
  const isBoss = computed(() => authStore.isBoss)
  const isAdmin = computed(() => authStore.isAdmin)
  const isMentor = computed(() => authStore.isMentor)

  const canManageStudents = computed(() => {
    return ['SUPERADMIN', 'BOSS', 'ADMIN'].includes(authStore.userRole)
  })

  const canManagePayments = computed(() => {
    return ['SUPERADMIN', 'BOSS', 'ADMIN'].includes(authStore.userRole)
  })

  const canViewAnalytics = computed(() => {
    return ['SUPERADMIN', 'BOSS'].includes(authStore.userRole)
  })

  const canManageAllowlist = computed(() => {
    return ['SUPERADMIN', 'BOSS'].includes(authStore.userRole)
  })

  return {
    isAuthenticated,
    user,
    userRole,
    isSuperAdmin,
    isBoss,
    isAdmin,
    isMentor,
    canManageStudents,
    canManagePayments,
    canViewAnalytics,
    canManageAllowlist,
  }
}

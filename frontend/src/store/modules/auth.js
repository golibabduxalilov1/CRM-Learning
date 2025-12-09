import { defineStore } from 'pinia'
import authService from '@/services/auth.service'
import websocketService from '@/services/websocket.service'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: (() => {
      try {
        const cached = localStorage.getItem('user')
        return cached ? JSON.parse(cached) : null
      } catch (error) {
        console.warn('Failed to parse cached user', error)
        return null
      }
    })(),
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    isAuthenticated: !!localStorage.getItem('access_token'),
    loading: false,
    error: null,
  }),

  getters: {
    userRole: (state) => state.user?.role,
    isSuperAdmin: (state) => state.user?.role === 'SUPERADMIN',
    isBoss: (state) => state.user?.role === 'BOSS',
    isAdmin: (state) => state.user?.role === 'ADMIN',
    isMentor: (state) => state.user?.role === 'MENTOR',
    fullName: (state) => {
      if (!state.user) return ''
      return `${state.user.first_name} ${state.user.last_name}`
    },
  },

  actions: {
    async register(data) {
      this.loading = true
      this.error = null
      try {
        await authService.register(data)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || "Ro'yxatdan o'tishda xatolik"
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async login(credentials) {
      this.loading = true
      this.error = null
      try {
        const response = await authService.login(credentials)
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.response?.data || 'Login xatolik'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async verifyOTP(data) {
      this.loading = true
      this.error = null
      try {
        const response = await authService.verifyOTP(data)
        const { access, refresh, user } = response.data

        this.accessToken = access
        this.refreshToken = refresh
        this.user = user
        this.isAuthenticated = true

        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        localStorage.setItem('user', JSON.stringify(user))

        websocketService.connect(access)

        router.push('/dashboard')
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || 'OTP tasdiqlash xatolik'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        await authService.logout()
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.clearSession()
        router.push('/login')
      }
    },

    clearSession() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      this.isAuthenticated = false

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')

      websocketService.disconnect()
    },

    async fetchCurrentUser(options = {}) {
      const { force = false } = options

      const cachedUser = localStorage.getItem('user')
      if (cachedUser && !force) {
        try {
          this.user = JSON.parse(cachedUser)
          return
        } catch (error) {
          console.warn('Failed to parse cached user', error)
          localStorage.removeItem('user')
        }
      }

      if (!this.accessToken) {
        return
      }

      try {
        const response = await authService.getCurrentUser()
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
      } catch (error) {
        console.error('Fetch user error:', error)
        if (error.response?.status === 401) {
          this.logout()
        }
      }
    },
  },
})

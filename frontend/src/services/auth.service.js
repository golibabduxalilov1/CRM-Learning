import api from './api'

export default {
  register(data) {
    return api.post('/auth/register/', data)
  },

  login(credentials) {
    return api.post('/auth/login/', credentials)
  },

  verifyOTP(data) {
    return api.post('/auth/otp/verify/', data)
  },

  logout() {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      return Promise.resolve()
    }
    return api.post('/auth/logout/', { refresh: refreshToken })
  },

  refreshToken(refresh) {
    return api.post('/auth/token/refresh/', { refresh })
  },

  getCurrentUser() {
    return api.get('/auth/me/')
  },

  updateProfile(data) {
    return api.patch('/auth/profile/', data)
  },

  changePassword(data) {
    return api.post('/auth/password/change/', data)
  },
}

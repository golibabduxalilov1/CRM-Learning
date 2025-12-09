import api from './api'

export default {
  getAll(params) {
    return api.get('/auth/users/', { params })
  },

  getByRole(role, params) {
    return api.get(`/auth/users/${role}/`, { params })
  },
}

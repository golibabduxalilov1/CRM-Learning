import api from './api'

export default {
  getAll(params) {
    return api.get('/students/', { params })
  },

  getById(id) {
    return api.get(`/students/${id}/`)
  },

  create(data) {
    return api.post('/students/', data)
  },

  update(id, data) {
    return api.put(`/students/${id}/`, data)
  },

  partialUpdate(id, data) {
    return api.patch(`/students/${id}/`, data)
  },

  delete(id) {
    return api.delete(`/students/${id}/`)
  },

  search(query) {
    return api.get('/students/', { params: { search: query } })
  },
}

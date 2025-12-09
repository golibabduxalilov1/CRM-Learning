import api from './api'

export default {
  getAll(params) {
    return api.get('/payouts/mentor/', { params })
  },

  getById(id) {
    return api.get(`/payouts/mentor/${id}/`)
  },

  generate(data) {
    return api.post('/payouts/mentor/generate/', data)
  },

  markPaid(id, data) {
    return api.patch(`/payouts/mentor/${id}/paid/`, data)
  },
}

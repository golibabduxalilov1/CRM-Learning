import api from './api'

export default {
  getAll(params) {
    return api.get('/payments/', { params })
  },

  getById(id) {
    return api.get(`/payments/${id}/`)
  },

  create(data) {
    return api.post('/payments/', data)
  },

  update(id, data) {
    return api.put(`/payments/${id}/`, data)
  },

  updateStatus(id, data) {
    return api.patch(`/payments/${id}/status/`, data)
  },

  delete(id) {
    return api.delete(`/payments/${id}/`)
  },

  getCommissionSettings() {
    return api.get('/payments/commission/global/')
  },

  updateCommissionSettings(data) {
    return api.patch('/payments/commission/global/', data)
  },

  updateGroupCommission(groupId, data) {
    return api.put(`/payments/commission/group/${groupId}/`, data)
  },

  updateMentorCommission(mentorId, data) {
    return api.put(`/payments/commission/mentor/${mentorId}/`, data)
  },
}

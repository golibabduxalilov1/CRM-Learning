import api from './api'

export default {
  getAll(params) {
    return api.get('/groups/', { params })
  },

  getById(id) {
    return api.get(`/groups/${id}/`)
  },

  create(data) {
    return api.post('/groups/', data)
  },

  update(id, data) {
    return api.put(`/groups/${id}/`, data)
  },

  delete(id) {
    return api.delete(`/groups/${id}/`)
  },

  assignMentor(groupId, mentorId) {
    return api.post(`/groups/${groupId}/assign-mentor/`, { mentor_id: mentorId })
  },

  getEnrollments(params) {
    return api.get('/groups/enrollments/', { params })
  },

  createEnrollment(data) {
    return api.post('/groups/enrollments/', data)
  },

  updateEnrollment(id, data) {
    return api.patch(`/groups/enrollments/${id}/`, data)
  },

  deleteEnrollment(id) {
    return api.delete(`/groups/enrollments/${id}/`)
  },
}

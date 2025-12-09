import api from './api'

const BASE_PATH = '/auth/allowlist/'

export default {
  getAll() {
    return api.get(BASE_PATH)
  },

  create(payload) {
    return api.post(BASE_PATH, payload)
  },

  delete(id) {
    return api.delete(`${BASE_PATH}${id}/`)
  },
}

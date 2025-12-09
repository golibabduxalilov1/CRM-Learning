import api from './api'

const BASE = '/dashboard'

export default {
  getRevenueSummary(params) {
    return api.get(`${BASE}/revenue/`, { params })
  },

  getMonthlyRevenue(params) {
    return api.get(`${BASE}/revenue/monthly/`, { params })
  },

  getStudentsPerGroup() {
    return api.get(`${BASE}/students-per-group/`)
  },

  getMentorPerformance() {
    return api.get(`${BASE}/mentor-performance/`)
  },

  getPaymentStatus() {
    return api.get(`${BASE}/payment-status/`)
  },

  getEnrollmentTrends(params) {
    return api.get(`${BASE}/enrollment-trends/`, { params })
  },
}

import { defineStore } from 'pinia'
import analyticsService from '@/services/analytics.service'

export const useAnalyticsStore = defineStore('analytics', {
  state: () => ({
    revenueSummary: null,
    monthlyRevenue: [],
    studentsPerGroup: [],
    mentorPerformance: [],
    paymentStatus: [],
    enrollmentTrends: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchRevenueSummary(params = {}) {
      this.loading = true
      try {
        const response = await analyticsService.getRevenueSummary(params)
        this.revenueSummary = response.data
      } catch (error) {
        this.error = error.response?.data
      } finally {
        this.loading = false
      }
    },

    async fetchMonthlyRevenue(params = {}) {
      try {
        const response = await analyticsService.getMonthlyRevenue(params)
        this.monthlyRevenue = response.data
      } catch (error) {
        this.error = error.response?.data
      }
    },

    async fetchStudentsPerGroup() {
      try {
        const response = await analyticsService.getStudentsPerGroup()
        this.studentsPerGroup = response.data
      } catch (error) {
        this.error = error.response?.data
      }
    },

    async fetchMentorPerformance() {
      try {
        const response = await analyticsService.getMentorPerformance()
        this.mentorPerformance = response.data
      } catch (error) {
        this.error = error.response?.data
      }
    },

    async fetchPaymentStatus() {
      try {
        const response = await analyticsService.getPaymentStatus()
        this.paymentStatus = response.data
      } catch (error) {
        this.error = error.response?.data
      }
    },

    async fetchEnrollmentTrends(params = {}) {
      try {
        const response = await analyticsService.getEnrollmentTrends(params)
        this.enrollmentTrends = response.data
      } catch (error) {
        this.error = error.response?.data
      }
    },

    async fetchAllDashboardData() {
      this.loading = true
      try {
        await Promise.all([
          this.fetchRevenueSummary(),
          this.fetchMonthlyRevenue({ months: 12 }),
          this.fetchStudentsPerGroup(),
          this.fetchMentorPerformance(),
          this.fetchPaymentStatus(),
          this.fetchEnrollmentTrends({ days: 30 }),
        ])
      } catch (error) {
        this.error = error
      } finally {
        this.loading = false
      }
    },
  },
})

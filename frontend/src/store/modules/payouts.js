import { defineStore } from 'pinia'
import payoutService from '@/services/payout.service'

export const usePayoutStore = defineStore('payouts', {
  state: () => ({
    payouts: [],
    currentPayout: null,
    loading: false,
    error: null,
    pagination: {
      count: 0,
      totalPages: 0,
      currentPage: 1,
    },
  }),

  getters: {
    calculatedPayouts: (state) => {
      return state.payouts.filter(p => p.status === 'CALCULATED')
    },
    paidPayouts: (state) => {
      return state.payouts.filter(p => p.status === 'PAID')
    },
    totalCalculated: (state) => {
      return state.payouts
        .filter(p => p.status === 'CALCULATED')
        .reduce((sum, p) => sum + Number(p.mentor_share), 0)
    },
    totalPaid: (state) => {
      return state.payouts
        .filter(p => p.status === 'PAID')
        .reduce((sum, p) => sum + Number(p.mentor_share), 0)
    },
  },

  actions: {
    async fetchPayouts(params = {}) {
      this.loading = true
      this.error = null
      try {
        const response = await payoutService.getAll(params)
        this.payouts = response.data.results || response.data
        this.pagination = {
          count: response.data.count || this.payouts.length,
          totalPages: response.data.total_pages || 1,
          currentPage: response.data.current_page || 1,
        }
      } catch (error) {
        this.error = error.response?.data || "To'lovlarni yuklashda xatolik"
      } finally {
        this.loading = false
      }
    },

    async fetchPayoutById(id) {
      this.loading = true
      this.error = null
      try {
        const response = await payoutService.getById(id)
        this.currentPayout = response.data
      } catch (error) {
        this.error = error.response?.data
      } finally {
        this.loading = false
      }
    },

    async generatePayout(data) {
      this.loading = true
      this.error = null
      try {
        await payoutService.generate(data)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async markPaid(id, data) {
      this.loading = true
      this.error = null
      try {
        await payoutService.markPaid(id, data)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },
  },
})

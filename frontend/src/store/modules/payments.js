import { defineStore } from 'pinia'
import paymentService from '@/services/payment.service'

export const usePaymentStore = defineStore('payments', {
  state: () => ({
    payments: [],
    currentPayment: null,
    loading: false,
    error: null,
    pagination: {
      count: 0,
      totalPages: 0,
      currentPage: 1,
    },
    commissionSettings: null,
  }),

  getters: {
    pendingPayments: (state) => {
      return state.payments.filter(p => p.status === 'PENDING')
    },
    paidPayments: (state) => {
      return state.payments.filter(p => p.status === 'PAID')
    },
    overduePayments: (state) => {
      return state.payments.filter(p => p.status === 'OVERDUE')
    },
    totalPending: (state) => {
      return state.payments
        .filter(p => p.status === 'PENDING')
        .reduce((sum, p) => sum + Number(p.amount), 0)
    },
    totalPaid: (state) => {
      return state.payments
        .filter(p => p.status === 'PAID')
        .reduce((sum, p) => sum + Number(p.amount), 0)
    },
  },

  actions: {
    async fetchPayments(params = {}) {
      this.loading = true
      this.error = null
      try {
        const response = await paymentService.getAll(params)
        this.payments = response.data.results || response.data
        this.pagination = {
          count: response.data.count || this.payments.length,
          totalPages: response.data.total_pages || 1,
          currentPage: response.data.current_page || 1,
        }
      } catch (error) {
        this.error = error.response?.data || "To'lovlarni yuklashda xatolik"
      } finally {
        this.loading = false
      }
    },

    async fetchPaymentById(id) {
      this.loading = true
      this.error = null
      try {
        const response = await paymentService.getById(id)
        this.currentPayment = response.data
      } catch (error) {
        this.error = error.response?.data
      } finally {
        this.loading = false
      }
    },

    async createPayment(data) {
      this.loading = true
      this.error = null
      try {
        await paymentService.create(data)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updatePaymentStatus(id, data) {
      this.loading = true
      this.error = null
      try {
        await paymentService.updateStatus(id, data)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || "To'lov holatini yangilashda xatolik"
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updatePayment(id, data) {
      this.loading = true
      this.error = null
      try {
        await paymentService.update(id, data)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || "To'lovni yangilashda xatolik"
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deletePayment(id) {
      this.loading = true
      this.error = null
      try {
        await paymentService.delete(id)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchCommissionSettings() {
      try {
        const response = await paymentService.getCommissionSettings()
        this.commissionSettings = response.data
      } catch (error) {
        this.error = error.response?.data
      }
    },

    async updateCommissionSettings(data) {
      this.loading = true
      this.error = null
      try {
        await paymentService.updateCommissionSettings(data)
        await this.fetchCommissionSettings()
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

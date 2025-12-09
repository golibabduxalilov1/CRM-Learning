import { defineStore } from 'pinia'
import allowlistService from '@/services/allowlist.service'

export const useAllowlistStore = defineStore('allowlist', {
  state: () => ({
    entries: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchEntries() {
      this.loading = true
      this.error = null
      try {
        const response = await allowlistService.getAll()
        this.entries = response.data.results || response.data
      } catch (error) {
        this.error = error.response?.data || 'Allowlist ma\'lumotlarini yuklashda xatolik'
      } finally {
        this.loading = false
      }
    },

    async addEntry(payload) {
      this.loading = true
      this.error = null
      try {
        await allowlistService.create(payload)
        await this.fetchEntries()
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || 'Allowlistga qo\'shishda xatolik'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async removeEntry(id) {
      this.loading = true
      this.error = null
      try {
        await allowlistService.delete(id)
        this.entries = this.entries.filter((entry) => entry.id !== id)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || 'Allowlistdan o\'chirishda xatolik'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },
  },
})

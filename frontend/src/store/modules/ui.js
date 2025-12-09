import { defineStore } from 'pinia'

export const useUIStore = defineStore('ui', {
  state: () => ({
    notification: {
      show: false,
      type: 'info',
      title: '',
      message: '',
    },
    loading: false,
    sidebarOpen: true,
  }),

  actions: {
    showNotification({ type = 'info', title = '', message = '' }) {
      this.notification = {
        show: true,
        type,
        title,
        message,
      }
    },

    hideNotification() {
      this.notification.show = false
    },

    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    },

    setLoading(value) {
      this.loading = value
    },
  },
})

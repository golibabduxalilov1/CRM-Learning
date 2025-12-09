import { useUIStore } from '@/store/modules/ui'

export function useNotification() {
  const uiStore = useUIStore()

  const showSuccess = (message, title = 'Muvaffaqiyatli!') => {
    uiStore.showNotification({
      type: 'success',
      title,
      message,
    })
  }

  const showError = (message, title = 'Xatolik!') => {
    uiStore.showNotification({
      type: 'error',
      title,
      message,
    })
  }

  const showInfo = (message, title = 'Ma\'lumot') => {
    uiStore.showNotification({
      type: 'info',
      title,
      message,
    })
  }

  const showWarning = (message, title = 'Ogohlantirish!') => {
    uiStore.showNotification({
      type: 'warning',
      title,
      message,
    })
  }

  return {
    showSuccess,
    showError,
    showInfo,
    showWarning,
  }
}

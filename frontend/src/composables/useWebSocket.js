import { onMounted, onUnmounted } from 'vue'
import websocketService from '@/services/websocket.service'
import { useAuthStore } from '@/store/modules/auth'

export function useWebSocket() {
  const authStore = useAuthStore()

  onMounted(() => {
    if (authStore.isAuthenticated && authStore.accessToken) {
      websocketService.connect(authStore.accessToken, authStore.userRole)
    }
  })

  onUnmounted(() => {
    websocketService.disconnect()
  })

  const onNotification = (callback) => {
    websocketService.on('notification', callback)
    
    return () => {
      websocketService.off('notification', callback)
    }
  }

  const onDashboardUpdate = (callback) => {
    websocketService.on('dashboard_update', callback)
    
    return () => {
      websocketService.off('dashboard_update', callback)
    }
  }

  return {
    onNotification,
    onDashboardUpdate,
  }
}

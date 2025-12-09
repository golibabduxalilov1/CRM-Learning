<template>
  <div id="app">
    <Notification
      :show="uiStore.notification.show"
      :type="uiStore.notification.type"
      :title="uiStore.notification.title"
      :message="uiStore.notification.message"
      @close="uiStore.hideNotification"
    />

    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/store/modules/auth'
import { useUIStore } from '@/store/modules/ui'
import Notification from '@/components/common/Notification.vue'

const authStore = useAuthStore()
const uiStore = useUIStore()

onMounted(() => {
  if (authStore.isAuthenticated) {
    authStore.fetchCurrentUser()
  }
})
</script>

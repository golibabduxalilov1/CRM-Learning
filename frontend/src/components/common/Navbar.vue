<template>
  <nav class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center h-16">
        <!-- Left section: logo & sidebar toggle -->
        <div class="flex items-center space-x-4">
          <!-- Mobile sidebar toggle -->
          <button
            v-if="authStore.isAuthenticated"
            class="lg:hidden p-2 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring rounded-md"
            aria-label="Open sidebar"
            @click="uiStore.toggleSidebar"
          >
            <Bars3Icon class="w-6 h-6 text-gray-700" />
          </button>

          <!-- Logo -->
          <router-link
            to="/"
            class="flex items-center space-x-2"
          >
            <AcademicCapIcon class="w-8 h-8 text-primary-600" />
            <span class="text-xl font-bold text-gray-900">Training&nbsp;CRM</span>
          </router-link>
        </div>

        <!-- Right section: notifications & user menu -->
        <div
          v-if="authStore.isAuthenticated"
          class="flex items-center space-x-4"
        >
          <!-- Notifications -->
          <div class="relative">
            <button
              class="relative p-2 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring rounded-md"
              aria-label="Open notifications"
              @click.stop="toggleNotifications"
            >
              <BellIcon class="w-6 h-6 text-gray-600" />
              <span
                v-if="unreadNotifications"
                class="absolute top-1 right-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[10px] font-semibold text-white"
              >
                {{ unreadNotifications > 9 ? '9+' : unreadNotifications }}
              </span>
            </button>

            <Transition name="dropdown">
              <div
                v-if="showNotifications"
                v-click-outside="closeNotifications"
                class="absolute right-0 mt-3 w-80 rounded-2xl border border-gray-200 bg-white shadow-xl z-50"
                @click.stop
              >
                <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
                  <div>
                    <p class="text-sm font-semibold text-gray-900">Bildirishnomalar</p>
                    <p class="text-xs text-gray-500">So'nggi yangiliklar va eslatmalar</p>
                  </div>
                  <button
                    class="text-xs font-medium text-primary-600 hover:text-primary-700 p-2 rounded-md"
                    @click.stop="markAllNotificationsRead"
                  >
                    O'qilgan
                  </button>
                </div>

                <div class="max-h-72 overflow-y-auto divide-y divide-gray-100">
                  <template v-if="notificationList.length">
                    <button
                      v-for="notification in notificationList"
                      :key="notification.id"
                      class="flex w-full items-start gap-3 px-4 py-3 text-left hover:bg-gray-50 p-2 rounded-md"
                      :class="{ 'bg-primary-50': !notification.read }"
                      @click="openNotification(notification.id)"
                    >
                      <span
                        class="mt-1 h-2 w-2 rounded-full"
                        :class="notification.read ? 'bg-gray-300' : 'bg-primary-500'"
                      />
                      <div class="flex-1">
                        <p class="text-sm font-semibold text-gray-900">
                          {{ notification.title }}
                        </p>
                        <p class="mt-1 text-xs text-gray-500">
                          {{ notification.message }}
                        </p>
                        <p class="mt-1 text-[11px] font-medium text-gray-400">
                          {{ notification.time }}
                        </p>
                      </div>
                    </button>
                  </template>

                  <div
                    v-else
                    class="px-4 py-8 text-center text-sm text-gray-500"
                  >
                    Hozircha bildirishnomalar mavjud emas.
                  </div>
                </div>

                <div class="border-t border-gray-100 p-3">
                  <button
                    class="block w-full rounded-xl bg-gray-50 px-4 py-2 text-center text-sm font-medium text-primary-600 hover:bg-primary-50 p-2 rounded-md"
                    @click="closeNotifications"
                  >
                    Bildirishnomalarni boshqarish
                  </button>
                </div>
              </div>
            </Transition>
          </div>

          <!-- User dropdown -->
          <div class="relative">
            <button
              class="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring rounded-md"
              aria-haspopup="true"
              :aria-expanded="showUserMenu.toString()"
              @click.stop="toggleUserMenu"
            >
              <div class="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                <span class="text-white font-semibold text-sm">{{ userInitials }}</span>
              </div>
              <div class="hidden md:block text-left">
                <p class="text-sm font-medium text-gray-900">
                  {{ fullName }}
                </p>
                <p class="text-xs text-gray-500">
                  {{ roleLabel }}
                </p>
              </div>
              <ChevronDownIcon class="w-5 h-5 text-gray-600" />
            </button>

            <Transition name="dropdown">
              <div
                v-if="showUserMenu"
                v-click-outside="closeUserMenu"
                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl border border-gray-200 py-1 z-50"
                @click.stop
              >
                <router-link
                  to="/settings/profile"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  @click="closeUserMenu"
                >
                  Profil
                </router-link>
                <router-link
                  v-if="canManageSettings"
                  to="/settings/commission"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  @click="closeUserMenu"
                >
                  Sozlamalar
                </router-link>
                <hr class="my-1">
                <button
                  class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 p-2 rounded-md"
                  @click="handleLogout"
                >
                  Chiqish
                </button>
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth'
import { useUIStore } from '@/store/modules/ui'
import { AcademicCapIcon, BellIcon, Bars3Icon, ChevronDownIcon } from '@heroicons/vue/24/outline'
import { getRoleLabel } from '@/utils/helpers'

/* Stores */
const authStore = useAuthStore()
const uiStore = useUIStore()
const route = useRoute()

/* UI state */
const showUserMenu = ref(false)
const showNotifications = ref(false)
const notificationItems = ref([
  {
    id: 1,
    title: 'Yangi interfeys',
    message: 'Dashboard dizayni yangilandi va yanada tezkor bo\'ldi.',
    time: 'Bugun 09:00',
    read: false,
  },
  {
    id: 2,
    title: 'To\'lov eslatmasi',
    message: '3 ta guruhda to\'lovlar kutilmoqda.',
    time: 'Kecha 17:20',
    read: true,
  },
])

/* Computed */
const userInitials = computed(() => {
  if (!authStore.user) return ''
  const first = authStore.user.first_name?.[0] ?? ''
  const last = authStore.user.last_name?.[0] ?? ''
  return `${first}${last}`.toUpperCase()
})

const fullName = computed(() =>
  authStore.user ? `${authStore.user.first_name} ${authStore.user.last_name}` : ''
)

const roleLabel = computed(() => getRoleLabel(authStore.user?.role))

const canManageSettings = computed(() =>
  ['SUPERADMIN', 'BOSS', 'ADMIN'].includes(authStore.userRole)
)

const notificationList = computed(() => notificationItems.value)
const unreadNotifications = computed(() => notificationItems.value.filter((item) => !item.read).length)

watch(
  () => authStore.user,
  (user) => {
    if (!user) return
    notificationItems.value = notificationItems.value.map((item) =>
      item.id === 1
        ? {
            ...item,
            message: `${user.first_name}, yangi dashboard imkoniyatlarini sinab ko'ring.`,
          }
        : item
    )
  },
  { immediate: true }
)

watch(
  () => uiStore.notification.show,
  (visible) => {
    if (visible) {
      const { title, message } = uiStore.notification
      notificationItems.value = [
        {
          id: Date.now(),
          title: title || 'Yangi bildirishnoma',
          message: message || 'Yangi xabar mavjud.',
          time: new Intl.DateTimeFormat('uz-UZ', {
            hour: '2-digit',
            minute: '2-digit',
          }).format(new Date()),
          read: false,
        },
        ...notificationItems.value,
      ].slice(0, 10)
    }
  }
)

/* Methods */
const toggleUserMenu = () => {
  showNotifications.value = false
  showUserMenu.value = !showUserMenu.value
}

const closeUserMenu = () => {
  showUserMenu.value = false
}

const toggleNotifications = () => {
  showUserMenu.value = false
  showNotifications.value = !showNotifications.value
}

const closeNotifications = () => {
  showNotifications.value = false
}

const openNotification = (notificationId) => {
  notificationItems.value = notificationItems.value.map((item) =>
    item.id === notificationId ? { ...item, read: true } : item
  )
}

const markAllNotificationsRead = () => {
  notificationItems.value = notificationItems.value.map((item) => ({ ...item, read: true }))
}

const handleLogout = async () => {
  closeUserMenu()
  closeNotifications()
  await authStore.logout()
}
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>

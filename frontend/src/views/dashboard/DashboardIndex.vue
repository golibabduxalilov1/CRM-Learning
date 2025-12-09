<template>
  <div class="relative flex min-h-screen bg-slate-50">
    <!-- Background Elements -->
    <div class="pointer-events-none fixed inset-0 overflow-hidden z-0">
      <div
        class="absolute -left-[10%] top-[10%] h-[500px] w-[500px] rounded-full bg-primary-200/40 blur-[100px] animate-pulse-slow"
      />
      <div
        class="absolute bottom-[10%] right-[10%] h-[500px] w-[500px] rounded-full bg-secondary-200/40 blur-[100px] animate-pulse-slow"
        style="animation-delay: 1s"
      />
    </div>

    <Sidebar class="relative z-20" />

    <div class="relative z-10 flex flex-1 flex-col min-w-0">
      <Navbar />

      <main class="flex-1 px-4 py-8 lg:px-8 space-y-8">
        <!-- Hero Section -->
        <section
          class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary-600 via-primary-700 to-secondary-800 text-white shadow-xl shadow-primary-900/20"
        >
          <!-- Decorative patterns -->
          <div class="absolute inset-0 bg-[url('/patterns/grid.svg')] opacity-10"></div>
          <div class="absolute -right-20 -top-20 h-96 w-96 rounded-full bg-white/10 blur-3xl"></div>
          <div
            class="absolute -left-20 -bottom-20 h-80 w-80 rounded-full bg-secondary-500/20 blur-3xl"
          ></div>

          <div class="relative z-10 grid gap-8 p-8 lg:grid-cols-12 lg:gap-12 items-center">
            <div class="lg:col-span-7 space-y-6">
              <div>
                <div
                  class="inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-1 text-xs font-medium backdrop-blur-md border border-white/10 mb-4"
                >
                  <span class="relative flex h-2 w-2">
                    <span
                      class="animate-ping absolute inline-flex h-full w-full rounded-full bg-success-400 opacity-75"
                    ></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-success-500"></span>
                  </span>
                  {{ greeting }}
                </div>
                <h1 class="text-4xl font-bold tracking-tight lg:text-5xl mb-2">
                  {{ authStore.fullName || 'CRM Study Center' }}
                </h1>
                <p class="text-lg text-primary-100 max-w-xl leading-relaxed">
                  {{ welcomeSubtitle }}
                </p>
              </div>

              <div class="flex flex-wrap gap-3">
                <div
                  v-for="stat in heroStats"
                  :key="stat.label"
                  class="flex flex-col px-4 py-2 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10"
                >
                  <span
                    class="text-[10px] uppercase tracking-wider text-primary-200 font-semibold"
                    >{{ stat.label }}</span
                  >
                  <span class="text-sm font-bold">{{ stat.value }}</span>
                </div>
              </div>
            </div>

            <div class="lg:col-span-5 space-y-4">
              <!-- Profile Card -->
              <div class="glass-panel rounded-2xl p-5 !bg-white/10 !border-white/20 text-white">
                <div class="flex items-center justify-between mb-3">
                  <span class="text-sm font-medium text-white/90">Profil holati</span>
                  <span class="text-sm font-bold">{{ profileCompleteness }}%</span>
                </div>
                <div class="h-2.5 w-full rounded-full bg-black/20 backdrop-blur-sm overflow-hidden">
                  <div
                    class="h-full rounded-full bg-gradient-to-r from-success-400 to-success-500 shadow-[0_0_10px_rgba(34,197,94,0.5)] transition-all duration-1000 ease-out"
                    :style="{ width: `${profileCompleteness}%` }"
                  />
                </div>
                <p class="mt-3 text-xs text-white/70 leading-relaxed">
                  To'liq profil ma'lumotlari tizimdan samarali foydalanishga yordam beradi.
                </p>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <router-link
                  v-for="action in quickActions"
                  :key="action.label"
                  :to="action.to"
                  class="group flex flex-col gap-2 rounded-2xl bg-white/10 hover:bg-white/20 border border-white/10 p-4 transition-all duration-300 hover:-translate-y-0.5"
                >
                  <component
                    :is="action.icon"
                    class="h-5 w-5 text-primary-200 group-hover:text-white transition-colors"
                  />
                  <div>
                    <p class="text-sm font-bold">{{ action.label }}</p>
                    <p
                      class="text-[10px] text-white/60 group-hover:text-white/80 transition-colors"
                    >
                      {{ action.description }}
                    </p>
                  </div>
                </router-link>
              </div>
            </div>
          </div>
        </section>

        <!-- Dashboard Content -->
        <section class="space-y-6">
          <div class="flex flex-wrap items-center justify-between gap-4 px-1">
            <div>
              <h2 class="text-xl font-bold text-slate-800 flex items-center gap-2">
                <span class="w-1.5 h-6 rounded-full bg-primary-500"></span>
                Asosiy ko'rsatkichlar
              </h2>
              <p class="text-sm text-slate-500 mt-1 ml-3.5">Real vaqt rejimida tizim holati</p>
            </div>
            <button
              class="btn-secondary gap-2 rounded-xl !py-2 !px-4 !text-xs p-2"
              @click="handleManualRefresh"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-4 h-4"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99"
                />
              </svg>
              Yangilash
            </button>
          </div>

          <div class="relative min-h-[300px]">
            <Transition name="fade" mode="out-in">
              <component :is="activeDashboard" v-if="activeDashboard" :key="dashboardKey" />
              <div
                v-else
                class="flex flex-col items-center justify-center rounded-3xl border border-dashed border-slate-200 bg-slate-50/50 p-12 text-center"
              >
                <div
                  class="w-16 h-16 rounded-full bg-slate-100 flex items-center justify-center mb-4"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="w-8 h-8 text-slate-400"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z"
                    />
                  </svg>
                </div>
                <h3 class="text-lg font-semibold text-slate-900">Panel mavjud emas</h3>
                <p class="mt-2 text-sm text-slate-500 max-w-sm">
                  Sizning rolingiz uchun maxsus panel tayyorlanmagan. Iltimos, administrator bilan
                  bog'laning.
                </p>
              </div>
            </Transition>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useAuthStore } from '@/store/modules/auth'
import { useWebSocket } from '@/composables/useWebSocket'
import { useNotification } from '@/composables/useNotification'
import { getRoleLabel, formatDateTime } from '@/utils/helpers'
import Navbar from '@/components/common/Navbar.vue'
import Sidebar from '@/components/common/Sidebar.vue'
import BossDashboard from '@/components/dashboard/BossDashboard.vue'
import AdminDashboard from '@/components/dashboard/AdminDashboard.vue'
import MentorDashboard from '@/components/dashboard/MentorDashboard.vue'
import {
  UserGroupIcon,
  AcademicCapIcon,
  BanknotesIcon,
  Cog6ToothIcon,
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const { onNotification, onDashboardUpdate } = useWebSocket()
const { showInfo } = useNotification()

const dashboardKey = ref(0)

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Xayrli tong'
  if (hour < 18) return 'Assalomu alaykum'
  return 'Kechgi smena'
})

const welcomeSubtitle = computed(() =>
  authStore.isMentor
    ? "Darslar jadvali, guruhlar va payoutlar bir joyda yig'ilgan."
    : "Gruhlar, talabalar va moliyaviy ko'rsatkichlar bo'yicha tezkor qarorlar qabul qiling.",
)

const heroStats = computed(() => {
  const user = authStore.user || {}
  return [
    { label: 'Rol', value: getRoleLabel(user.role) || 'Aniqlanmagan' },
    { label: 'Email', value: user.email || 'Kiritilmagan' },
    {
      label: 'Oxirgi kirish',
      value: user.last_login ? formatDateTime(user.last_login) : 'Hali qayd etilmagan',
    },
  ]
})

const profileCompleteness = computed(() => {
  const user = authStore.user || {}
  const fields = ['email', 'phone', 'username']
  const filled = fields.filter((field) => !!user?.[field]).length
  return Math.max(35, Math.round((filled / fields.length) * 100) || 35)
})

const quickActions = computed(() => {
  if (authStore.isMentor) {
    return [
      {
        label: 'Guruhlarim',
        description: 'Jadval va darslar',
        to: '/groups',
        icon: AcademicCapIcon,
      },
      { label: 'Talabalar', description: "Faol ro'yxat", to: '/students', icon: UserGroupIcon },
      { label: 'Payoutlar', description: 'Oylik ulush', to: '/payouts', icon: BanknotesIcon },
      { label: 'Sozlamalar', description: 'Profil', to: '/settings/profile', icon: Cog6ToothIcon },
    ]
  }

  const base = [
    {
      label: 'Talabalar',
      description: "Ro'yxatni boshqarish",
      to: '/students',
      icon: UserGroupIcon,
    },
    { label: 'Guruhlar', description: 'Jadval va taqvim', to: '/groups', icon: AcademicCapIcon },
    {
      label: "To'lovlar",
      description: 'Monitoring va status',
      to: '/payments',
      icon: BanknotesIcon,
    },
  ]

  if (authStore.isBoss || authStore.isSuperAdmin || authStore.isAdmin) {
    base.push({
      label: 'Sozlamalar',
      description: 'Tizim boshqaruvi',
      to: '/settings/profile',
      icon: Cog6ToothIcon,
    })
  }

  return base
})

const activeDashboard = computed(() => {
  if (authStore.isBoss || authStore.isSuperAdmin) return BossDashboard
  if (authStore.isAdmin) return AdminDashboard
  if (authStore.isMentor) return MentorDashboard
  return null
})

const handleManualRefresh = () => {
  dashboardKey.value += 1
}

onMounted(() => {
  onNotification((data) => {
    showInfo(data.message, data.title)
  })

  onDashboardUpdate(() => {
    handleManualRefresh()
  })
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>

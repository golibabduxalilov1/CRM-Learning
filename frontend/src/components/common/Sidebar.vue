<template>
  <aside
    class="w-72 bg-white/80 backdrop-blur-xl border-r border-white/20 shadow-glass min-h-screen sticky top-0 overflow-y-auto z-40 transition-all duration-300"
    :class="{ '-translate-x-full lg:translate-x-0 fixed lg:sticky': !uiStore.sidebarOpen }"
  >
    <div class="p-6">
      <!-- Brand -->
      <div class="flex items-center gap-3 px-2 mb-8">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center text-white shadow-lg shadow-primary-500/30">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
            <path d="M11.7 2.805a.75.75 0 01.6 0A60.65 60.65 0 0122.83 8.72a.75.75 0 01-.231 1.337 49.949 49.949 0 00-9.902 3.912l-.003.002-.34.18a.75.75 0 01-.707 0A50.009 50.009 0 007.5 12.174v-.224c0-.131.067-.248.182-.311a49.853 49.853 0 0011.448-9.475.75.75 0 01.57-.164zM2.5 12a.75.75 0 01.75.75 49.83 49.83 0 002.428 10.584.75.75 0 01-.248.754A60.324 60.324 0 012.5 12zM12.75 12a49.828 49.828 0 009.375-6.125.75.75 0 01.75.75 60.353 60.353 0 01-9.375 6.125.75.75 0 01-.75-.75z" />
          </svg>
        </div>
        <div>
          <h1 class="text-lg font-bold text-slate-800 leading-tight">CRM System</h1>
          <p class="text-xs text-slate-500 font-medium">Study Center</p>
        </div>
      </div>

      <nav class="space-y-1.5">
        <router-link
          v-for="item in menuItems"
          :key="item.name"
          :to="item.path"
          class="group flex items-center gap-3 px-4 py-3.5 rounded-xl transition-all duration-300 relative overflow-hidden"
          :class="
            isActive(item.path)
              ? 'bg-primary-50 text-primary-700 font-semibold shadow-sm ring-1 ring-primary-100'
              : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
          "
        >
          <component
            :is="item.icon"
            class="w-5 h-5 transition-colors duration-300"
            :class="isActive(item.path) ? 'text-primary-600' : 'text-slate-400 group-hover:text-slate-600'"
          />
          <span class="relative z-10">{{ item.label }}</span>
          <span
            v-if="item.badge"
            class="ml-auto badge badge-primary relative z-10"
          >
            {{ item.badge }}
          </span>
          
          <!-- Active Indicator -->
          <div 
            v-if="isActive(item.path)"
            class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-primary-500 rounded-r-full"
          ></div>
        </router-link>

        <div
          v-if="settingsItems.length > 0"
          class="pt-6 mt-6 border-t border-slate-100"
        >
          <p class="px-4 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
            Sozlamalar
          </p>
          <router-link
            v-for="item in settingsItems"
            :key="item.name"
            :to="item.path"
            class="group flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 relative overflow-hidden"
            :class="
              isActive(item.path)
                ? 'bg-primary-50 text-primary-700 font-semibold shadow-sm ring-1 ring-primary-100'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            "
          >
            <component
              :is="item.icon"
              class="w-5 h-5 transition-colors duration-300"
              :class="isActive(item.path) ? 'text-primary-600' : 'text-slate-400 group-hover:text-slate-600'"
            />
            <span class="relative z-10">{{ item.label }}</span>
          </router-link>
        </div>
      </nav>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth'
import { useUIStore } from '@/store/modules/ui'
import {
  HomeIcon,
  UserGroupIcon,
  AcademicCapIcon,
  CurrencyDollarIcon,
  BanknotesIcon,
  Cog6ToothIcon,
  ShieldCheckIcon,
} from '@heroicons/vue/24/outline'

const route = useRoute()
const authStore = useAuthStore()
const uiStore = useUIStore()

const allMenuItems = [
  {
    name: 'dashboard',
    path: '/dashboard',
    label: 'Dashboard',
    icon: HomeIcon,
    roles: ['SUPERADMIN', 'BOSS', 'ADMIN', 'MENTOR'],
  },
  {
    name: 'students',
    path: '/students',
    label: 'Talabalar',
    icon: UserGroupIcon,
    roles: ['SUPERADMIN', 'BOSS', 'ADMIN', 'MENTOR'],
  },
  {
    name: 'groups',
    path: '/groups',
    label: 'Guruhlar',
    icon: AcademicCapIcon,
    roles: ['SUPERADMIN', 'BOSS', 'ADMIN', 'MENTOR'],
  },
  {
    name: 'payments',
    path: '/payments',
    label: "To'lovlar",
    icon: CurrencyDollarIcon,
    roles: ['SUPERADMIN', 'BOSS', 'ADMIN'],
  },
  {
    name: 'payouts',
    path: '/payouts',
    label: "To'lab berish",
    icon: BanknotesIcon,
    roles: ['SUPERADMIN', 'BOSS', 'ADMIN', 'MENTOR'],
  },
]

const allSettingsItems = [
  {
    name: 'commission',
    path: '/settings/commission',
    label: 'Komissiya',
    icon: Cog6ToothIcon,
    roles: ['SUPERADMIN', 'BOSS'],
  },
  {
    name: 'allowlist',
    path: '/settings/allowlist',
    label: 'Email Allowlist',
    icon: ShieldCheckIcon,
    roles: ['SUPERADMIN', 'BOSS'],
  },
]

const menuItems = computed(() =>
  allMenuItems.filter((item) => item.roles.includes(authStore.userRole))
)

const settingsItems = computed(() =>
  allSettingsItems.filter((item) => item.roles.includes(authStore.userRole))
)

const isActive = (path) => route.path.startsWith(path)
</script>

<template>
  <div class="space-y-8">
    <!-- Premium Hero Section -->
    <div
      class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary-600 via-primary-700 to-indigo-800 p-8 text-white shadow-xl shadow-primary-900/20"
    >
      <div class="absolute -left-20 -top-24 h-64 w-64 rounded-full bg-white/10 blur-3xl" />
      <div class="absolute -right-12 -bottom-20 h-72 w-72 rounded-full bg-indigo-400/20 blur-3xl" />
      <div
        class="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(255,255,255,0.12),transparent_35%),radial-gradient(circle_at_80%_0%,rgba(255,255,255,0.1),transparent_35%)]"
      />

      <div class="relative flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
        <div class="space-y-3">
          <div class="pill-soft">
            <span
              class="inline-flex h-2 w-2 rounded-full bg-emerald-300 shadow-[0_0_0_6px_rgba(16,185,129,0.25)]"
            />
            Strategik ko'rinish
          </div>
          <div>
            <h1 class="text-3xl font-bold tracking-tight md:text-4xl">Boss Dashboard</h1>
            <p class="mt-2 text-sm text-white/80 max-w-2xl">
              Moliyaviy oqimlar, guruhlar va mentorlar samaradorligini real vaqtda kuzating va
              tahlil qiling.
            </p>
          </div>
          <div class="flex flex-wrap gap-3">
            <span class="pill-soft">
              <ChartBarIcon class="h-4 w-4" />
              Real-time oqim
            </span>
            <span class="pill-soft">
              <ShieldCheckIcon class="h-4 w-4" />
              OTP + RBAC
            </span>
          </div>
        </div>
        <div
          class="glass-panel relative rounded-2xl border-white/20 bg-white/10 p-5 text-white shadow-[0_20px_60px_rgba(15,23,42,0.25)] backdrop-blur"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs font-semibold uppercase tracking-[0.25em] text-white/80">
                Oxirgi oy
              </p>
              <p class="mt-1 text-3xl font-extrabold">
                {{ insightChips[0]?.value || formatMoney(0) }}
              </p>
              <p class="text-sm text-white/70">Daromad dinamikasi</p>
            </div>
            <button
              class="inline-flex items-center gap-2 border border-white/30 bg-white/10 px-4 py-2 text-sm font-semibold text-white backdrop-blur transition hover:border-white/50 hover:bg-white/20 p-2 rounded-md"
              @click="refreshData"
            >
              <ArrowPathIcon class="w-5 h-5" />
              Yangilash
            </button>
          </div>
          <div class="mt-4 flex items-center gap-3 text-xs text-white/70">
            <span
              class="inline-flex items-center gap-1 rounded-full px-3 py-1 text-[11px] font-semibold"
              :class="
                insightChips[0]?.accentClass?.includes('success')
                  ? 'bg-emerald-500/20 text-emerald-50'
                  : 'bg-red-500/20 text-red-50'
              "
            >
              <component :is="insightChips[0]?.icon" class="h-4 w-4" />
              {{ insightChips[0]?.hint }}
            </span>
            <span>Oxirgi oyga nisbatan</span>
          </div>
        </div>
      </div>

      <div class="relative z-10 mt-8 grid gap-4 md:grid-cols-3">
        <div
          v-for="chip in insightChips"
          :key="chip.label"
          class="group rounded-2xl border border-white/15 bg-white/10 p-5 text-white backdrop-blur-md shadow-lg shadow-primary-900/10 transition hover:-translate-y-1 hover:border-white/30"
        >
          <div class="mb-3 flex items-start justify-between">
            <div class="text-[11px] font-semibold uppercase tracking-[0.2em] text-white/70">
              {{ chip.label }}
            </div>
            <component
              v-if="chip.icon"
              :is="chip.icon"
              class="h-5 w-5 text-primary-200 opacity-70 transition-opacity group-hover:opacity-100"
            />
          </div>
          <div class="mb-2 text-3xl font-bold text-white">
            {{ chip.value }}
          </div>
          <p class="text-sm" :class="chip.accentClass || 'text-white/80'">
            {{ chip.hint }}
          </p>
        </div>
      </div>
    </div>

    <Loading v-if="analyticsStore.loading" />

    <div v-else class="space-y-8">
      <!-- Enhanced Stats Grid -->
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">
        <StatCard
          v-for="stat in enhancedStats"
          :key="stat.title"
          :title="stat.title"
          :value="stat.value"
          :format="stat.format"
          :icon="stat.icon"
          :icon-bg-class="stat.iconBgClass"
          :icon-color-class="stat.iconColorClass"
          :subtitle="stat.subtitle"
          :trend="stat.trend"
          class="p-3"
        />
      </div>

      <!-- Charts Section -->
      <div class="grid gap-6 lg:grid-cols-3">
        <div class="lg:col-span-2 space-y-6">
          <RevenueChart :data="analyticsStore.monthlyRevenue" />
          <div class="grid gap-6 md:grid-cols-2">
            <PaymentStatusChart :data="analyticsStore.paymentStatus" class="p-4" />
            <StudentEnrollmentChart :data="analyticsStore.enrollmentTrends" class="p-4" />
          </div>
        </div>

        <!-- Enhanced Operational Focus -->
        <div class="card glass-panel h-full p-4">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-8 h-8 rounded-lg bg-primary-100 flex items-center justify-center">
              <ChartBarIcon class="w-5 h-5 text-primary-600" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-slate-900">Operatsion fokus</h3>
              <p class="text-xs text-slate-500">Ustuvorlik bo'yicha rejalashtiring</p>
            </div>
          </div>

          <div class="space-y-5">
            <div v-for="area in focusAreas" :key="area.title" class="group">
              <div
                class="flex items-center justify-between text-sm font-semibold text-slate-700 mb-2"
              >
                <span>{{ area.title }}</span>
                <span class="text-primary-600">{{ area.percent }}%</span>
              </div>
              <div class="relative h-3 w-full rounded-full bg-slate-100 overflow-hidden">
                <div
                  class="absolute inset-0 h-full rounded-full bg-gradient-to-r from-primary-500 to-primary-600 transition-all duration-500 group-hover:scale-x-105"
                  :style="{ width: `${area.percent}%` }"
                >
                  <div class="absolute inset-0 bg-white/20 animate-pulse"></div>
                </div>
              </div>
              <div class="mt-2 flex items-center justify-between text-xs">
                <span class="text-slate-500">{{ area.hint }}</span>
                <span class="font-semibold text-slate-700">{{ formatMoney(area.amount) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Enhanced Tables Section -->
      <div class="grid gap-6 lg:grid-cols-2">
        <!-- Mentor Performance Table -->
        <div class="card glass-panel p-4">
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-3">
              <div
                class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-100 to-primary-50 flex items-center justify-center"
              >
                <UserGroupIcon class="w-6 h-6 text-primary-600" />
              </div>
              <div>
                <h3 class="text-lg font-bold text-slate-900">Mentor samaradorligi</h3>
                <p class="text-sm text-slate-500">Guruhlar va daromad bo'yicha nazorat</p>
              </div>
            </div>
          </div>

          <div
            v-if="analyticsStore.mentorPerformance.length"
            class="overflow-hidden rounded-xl border border-slate-100"
          >
            <table class="min-w-full divide-y divide-slate-100">
              <thead class="bg-slate-50">
                <tr>
                  <th
                    class="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider"
                  >
                    Mentor
                  </th>
                  <th
                    class="px-4 py-3 text-center text-xs font-semibold text-slate-600 uppercase tracking-wider"
                  >
                    Guruhlar
                  </th>
                  <th
                    class="px-4 py-3 text-center text-xs font-semibold text-slate-600 uppercase tracking-wider"
                  >
                    Talabalar
                  </th>
                  <th
                    class="px-4 py-3 text-right text-xs font-semibold text-slate-600 uppercase tracking-wider"
                  >
                    Daromad
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-slate-50">
                <tr
                  v-for="mentor in analyticsStore.mentorPerformance"
                  :key="mentor.id"
                  class="hover:bg-slate-50 transition-colors"
                >
                  <td class="px-4 py-4">
                    <div class="flex items-center gap-3">
                      <div
                        class="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-primary-100 to-primary-50 text-primary-700 font-semibold text-sm"
                      >
                        {{ mentor.first_name?.[0] }}{{ mentor.last_name?.[0] }}
                      </div>
                      <div class="min-w-0">
                        <p class="font-semibold text-slate-900 truncate">
                          {{ mentor.first_name }} {{ mentor.last_name }}
                        </p>
                        <p class="text-xs text-slate-500">
                          {{ mentor.subject || 'Mentor' }}
                        </p>
                      </div>
                    </div>
                  </td>
                  <td class="px-4 py-4 text-center">
                    <span
                      class="inline-flex items-center justify-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-700"
                    >
                      {{ mentor.groups_count }}
                    </span>
                  </td>
                  <td class="px-4 py-4 text-center">
                    <span
                      class="inline-flex items-center justify-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-700"
                    >
                      {{ mentor.total_students }}
                    </span>
                  </td>
                  <td class="px-4 py-4 text-right font-semibold text-green-600">
                    {{ formatMoney(mentor.total_revenue) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div
            v-else
            class="rounded-2xl border border-dashed border-slate-200 bg-slate-50/80 p-8 text-center"
          >
            <UserGroupIcon class="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <p class="font-semibold text-slate-600">Mentor ma'lumotlari mavjud emas</p>
            <p class="text-sm text-slate-500 mt-1">
              Mentorlar performance moduli ulanmaguncha bu bo'lim bo'sh bo'ladi.
            </p>
          </div>
        </div>

        <!-- Students Per Group -->
        <div class="card glass-panel p-4">
          <div class="flex items-center gap-3 mb-6">
            <div
              class="w-10 h-10 rounded-xl bg-gradient-to-br from-secondary-100 to-secondary-50 flex items-center justify-center"
            >
              <AcademicCapIcon class="w-6 h-6 text-secondary-600" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-slate-900">Guruhlardagi talabalar</h3>
              <p class="text-sm text-slate-500">Sig'im va to'lish darajasi</p>
            </div>
          </div>

          <div class="space-y-4">
            <div
              v-for="group in analyticsStore.studentsPerGroup"
              :key="group.name"
              class="group rounded-2xl border border-slate-100 bg-slate-50/60 p-4 transition-all hover:border-primary-200 hover:bg-white hover:shadow-sm"
            >
              <div class="flex items-center justify-between mb-3">
                <h4 class="text-base font-semibold text-slate-900">
                  {{ group.name }}
                </h4>
                <span class="badge badge-primary text-xs">
                  {{ group.subject || 'Guruh' }}
                </span>
              </div>
              <p class="text-sm text-slate-500 mb-3">
                {{ group.mentor || 'Mentor belgilanmagan' }}
              </p>
              <div class="space-y-2">
                <div class="flex items-center justify-between text-sm">
                  <span class="text-slate-600">Talabalar</span>
                  <span class="font-semibold text-slate-900">
                    {{ group.active_students }} / {{ group.max_students || 'cheksiz' }}
                  </span>
                </div>
                <div class="relative h-2.5 rounded-full bg-white overflow-hidden">
                  <div
                    class="absolute inset-0 h-full rounded-full bg-gradient-to-r transition-all duration-500 group-hover:scale-x-105"
                    :class="getGroupCapacityClass(group)"
                    :style="{ width: getGroupCapacity(group) }"
                  >
                    <div class="absolute inset-0 bg-white/20 animate-pulse"></div>
                  </div>
                </div>
              </div>
            </div>
            <div
              v-if="!analyticsStore.studentsPerGroup.length"
              class="rounded-2xl border border-dashed border-slate-200 bg-white/70 p-8 text-center"
            >
              <AcademicCapIcon class="w-12 h-12 text-slate-300 mx-auto mb-3" />
              <p class="text-slate-500">Guruhlar statistikasi hozircha mavjud emas.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAnalyticsStore } from '@/store/modules/analytics'
import StatCard from './StatCard.vue'
import RevenueChart from './RevenueChart.vue'
import PaymentStatusChart from './PaymentStatusChart.vue'
import StudentEnrollmentChart from './StudentEnrollmentChart.vue'
import Loading from '@/components/common/Loading.vue'
import { formatMoney } from '@/utils/helpers'
import {
  CurrencyDollarIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon,
  ArrowPathIcon,
  ChartBarIcon,
  UserGroupIcon,
  AcademicCapIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  ShieldCheckIcon,
} from '@heroicons/vue/24/outline'

const analyticsStore = useAnalyticsStore()

// Enhanced stats with trends
const enhancedStats = computed(() => {
  const summary = analyticsStore.revenueSummary || {}

  return [
    {
      title: 'Umumiy daromad',
      value: summary.total_revenue || 0,
      format: 'money',
      icon: CurrencyDollarIcon,
      iconBgClass: 'bg-green-100',
      iconColorClass: 'text-green-600',
      subtitle: "Tasdiqlangan to'lovlar",
      trend: calculateTrend('revenue'),
    },
    {
      title: "Kutilayotgan to'lovlar",
      value: summary.pending_amount || 0,
      format: 'money',
      icon: ClockIcon,
      iconBgClass: 'bg-yellow-100',
      iconColorClass: 'text-yellow-600',
      subtitle: 'Tasdiqlanishi kerak',
      trend: null,
    },
    {
      title: "Muddati o'tgan",
      value: summary.overdue_amount || 0,
      format: 'money',
      icon: ExclamationTriangleIcon,
      iconBgClass: 'bg-red-100',
      iconColorClass: 'text-red-600',
      subtitle: 'Shoshilinch nazorat',
      trend: null,
    },
    {
      title: "To'lovlar soni",
      value: summary.payment_count || 0,
      format: 'number',
      icon: DocumentTextIcon,
      iconBgClass: 'bg-blue-100',
      iconColorClass: 'text-blue-600',
      subtitle: "Jami to'lovlar",
      trend: calculateTrend('payments'),
    },
  ]
})

const calculateTrend = (type) => {
  const monthly = analyticsStore.monthlyRevenue || []
  if (monthly.length < 2) return null

  const lastEntry = monthly[monthly.length - 1]
  const prevEntry = monthly[monthly.length - 2]

  if (!lastEntry || !prevEntry) return null

  const lastValue = type === 'revenue' ? lastEntry.revenue : lastEntry.count
  const prevValue = type === 'revenue' ? prevEntry.revenue : prevEntry.count

  if (!prevValue) return null

  return (((lastValue - prevValue) / prevValue) * 100).toFixed(1)
}

const insightChips = computed(() => {
  const monthly = analyticsStore.monthlyRevenue || []
  const lastEntry = monthly[monthly.length - 1]
  const prevEntry = monthly[monthly.length - 2]
  const lastRevenue = lastEntry?.revenue || 0
  const prevRevenue = prevEntry?.revenue || lastRevenue || 1
  const diff = prevRevenue ? (((lastRevenue - prevRevenue) / prevRevenue) * 100).toFixed(1) : 0
  const formatNumber = (value) => new Intl.NumberFormat('uz-UZ').format(value || 0)

  return [
    {
      label: 'Oxirgi oy daromadi',
      value: formatMoney(lastRevenue),
      hint: `${diff >= 0 ? "O'sish" : 'Pasayish'} ${Math.abs(diff)}%`,
      accentClass: diff >= 0 ? 'text-success-600' : 'text-danger-600',
      icon: diff >= 0 ? ArrowTrendingUpIcon : ArrowTrendingDownIcon,
    },
    {
      label: 'Faol guruhlar',
      value: formatNumber(analyticsStore.studentsPerGroup.length || 0),
      hint: 'Nazorat ostidagi guruhlar',
      accentClass: 'text-primary-600',
      icon: AcademicCapIcon,
    },
    {
      label: 'Mentorlar',
      value: formatNumber(analyticsStore.mentorPerformance.length || 0),
      hint: 'Samaradorlik monitoringi',
      accentClass: 'text-slate-600',
      icon: UserGroupIcon,
    },
  ]
})

const focusAreas = computed(() => {
  const summary = analyticsStore.revenueSummary || {}
  const total =
    (summary.total_revenue || 0) + (summary.pending_amount || 0) + (summary.overdue_amount || 0)

  const calcPercent = (amount) => {
    if (!total) return 0
    return Math.max(0, Math.round((amount / total) * 100))
  }

  return [
    {
      title: "Kutilayotgan to'lovlar",
      amount: summary.pending_amount || 0,
      percent: calcPercent(summary.pending_amount || 0),
      hint: 'Tasdiqlanishi kerak',
    },
    {
      title: "Muddati o'tgan to'lovlar",
      amount: summary.overdue_amount || 0,
      percent: calcPercent(summary.overdue_amount || 0),
      hint: 'Shoshilinch nazorat',
    },
    {
      title: 'Jami daromad',
      amount: summary.total_revenue || 0,
      percent: calcPercent(summary.total_revenue || 0),
      hint: 'Yuqori daromad aylanishi',
    },
  ]
})

const getGroupCapacity = (group) => {
  if (!group.max_students) return '100%'
  const percent = Math.min(100, Math.round((group.active_students / group.max_students) * 100))
  return `${percent}%`
}

const getGroupCapacityClass = (group) => {
  if (!group.max_students) return 'from-primary-500 to-primary-600'
  const percent = (group.active_students / group.max_students) * 100
  if (percent >= 90) return 'from-red-500 to-red-600'
  if (percent >= 70) return 'from-yellow-500 to-yellow-600'
  return 'from-green-500 to-green-600'
}

onMounted(() => {
  refreshData()
})

const refreshData = () => {
  analyticsStore.fetchAllDashboardData()
}
</script>

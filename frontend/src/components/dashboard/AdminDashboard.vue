<template>
  <div class="space-y-8">
    <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary-600 via-primary-700 to-indigo-800 p-8 text-white shadow-xl shadow-primary-900/20">
      <div class="absolute -left-20 -top-24 h-64 w-64 rounded-full bg-white/10 blur-3xl" />
      <div class="absolute -right-12 -bottom-20 h-72 w-72 rounded-full bg-indigo-400/20 blur-3xl" />
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(255,255,255,0.12),transparent_35%),radial-gradient(circle_at_80%_0%,rgba(255,255,255,0.1),transparent_35%)]" />

      <div class="relative flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
        <div class="space-y-3">
          <div class="pill-soft">
            <span class="inline-flex h-2 w-2 rounded-full bg-emerald-300 shadow-[0_0_0_6px_rgba(16,185,129,0.25)]" />
            Administrator rejimi
          </div>
          <div>
            <h1 class="text-3xl font-bold tracking-tight md:text-4xl">Admin Dashboard</h1>
            <p class="mt-2 text-sm text-white/80 max-w-2xl">
              Kundalik operatsiyalar, talabalar va to'lovlarni bir joydan boshqaring. Real-time ko'rsatkichlar va xavfsiz ruxsatlar bilan avtomatlashtirilgan jarayonlar.
            </p>
          </div>
          <div class="flex flex-wrap gap-3">
            <span class="pill-soft">
              <ClockIcon class="h-4 w-4" />
              Operatsion tezlik
            </span>
            <span class="pill-soft">
              <ShieldCheckIcon class="h-4 w-4" />
              OTP + RBAC
            </span>
          </div>
        </div>

        <div class="glass-panel relative rounded-2xl border-white/20 bg-white/10 p-5 text-left text-white shadow-[0_20px_60px_rgba(15,23,42,0.25)] backdrop-blur">
          <p class="text-xs font-semibold uppercase tracking-[0.25em] text-white/80">Bugungi sharh</p>
          <p class="mt-2 text-3xl font-extrabold">{{ pulseMetrics[0]?.value || 0 }}</p>
          <p class="text-sm text-white/70">Yangi enrollments / 5 ta oxirgi yozuv</p>
          <div class="mt-4 h-2 w-full overflow-hidden rounded-full bg-white/10">
            <div class="h-full w-3/4 rounded-full bg-gradient-to-r from-emerald-300 to-white/80" />
          </div>
        </div>
      </div>

      <div class="relative mt-6 grid gap-4 sm:grid-cols-3">
        <div
          v-for="metric in pulseMetrics"
          :key="metric.label"
          class="rounded-2xl border border-white/15 bg-white/10 p-4 backdrop-blur-md shadow-lg shadow-primary-900/10 transition hover:-translate-y-0.5 hover:border-white/30"
        >
          <p class="text-[11px] font-semibold uppercase tracking-[0.2em] text-white/70">
            {{ metric.label }}
          </p>
          <p class="mt-1 text-2xl font-bold text-white">
            {{ metric.value }}
          </p>
          <p class="mt-2 text-sm text-white/70">
            {{ metric.hint }}
          </p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
      <StatCard
        title="Jami talabalar"
        :value="studentStore.pagination.count"
        format="number"
        subtitle="Ro'yxatdan o'tganlar"
        :icon="UserGroupIcon"
      />
      <StatCard
        title="Faol guruhlar"
        :value="groupStore.totalGroups || groupStore.groups.length"
        format="number"
        subtitle="Hozirgi guruhlar"
        :icon="AcademicCapIcon"
      />
      <StatCard
        title="Kutilayotgan to'lovlar"
        :value="analyticsStore.revenueSummary?.pending_amount || 0"
        format="money"
        subtitle="Tasdiqlanmagan to'lovlar"
        :icon="ClockIcon"
        icon-bg-class="bg-yellow-100"
        icon-color-class="text-yellow-600"
      />
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="card glass-panel">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-bold text-slate-900">
              So'nggi yozilganlar
            </h3>
            <p class="text-sm text-slate-500">
              Oxirgi 5 ta ro'yxatdan o'tish
            </p>
          </div>
          <span class="rounded-full bg-primary-100 px-3 py-1 text-xs font-semibold text-primary-700">
            Live
          </span>
        </div>
        <div class="mt-5 space-y-4">
          <div
            v-for="enrollment in recentEnrollments"
            :key="enrollment.id"
            class="flex items-center justify-between rounded-2xl border border-slate-100 bg-slate-50/60 p-4 transition hover:border-primary-200"
          >
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary-100 text-primary-700">
                <span class="text-sm font-semibold">{{ enrollment.student_name?.[0] || '?' }}</span>
              </div>
              <div>
                <p class="text-base font-semibold text-slate-900">
                  {{ enrollment.student_name }}
                </p>
                <p class="text-sm text-slate-500">
                  {{ enrollment.group_name }}
                </p>
              </div>
            </div>
            <div class="text-right text-sm">
              <p class="font-semibold text-slate-900">
                {{ formatDate(enrollment.enrolled_date) }}
              </p>
              <p class="text-xs text-slate-500">
                Yozilgan sana
              </p>
            </div>
          </div>
          <div
            v-if="!recentEnrollments.length"
            class="rounded-2xl border border-dashed border-slate-200 bg-white/70 p-6 text-center text-slate-500"
          >
            Yaqinda ro'yxatdan o'tgan talabalar mavjud emas.
          </div>
        </div>
      </div>

      <div class="card glass-panel">
        <div class="flex items-center gap-2">
          <ExclamationTriangleIcon class="w-5 h-5 text-danger-600" />
          <h3 class="text-lg font-bold text-slate-900">
            Muddati o'tgan to'lovlar
          </h3>
        </div>
        <p class="text-sm text-slate-500">
          Ularni birinchi bo'lib tasdiqlang.
        </p>
        <div class="mt-5 space-y-4">
          <div
            v-for="payment in overduePayments"
            :key="payment.id"
            class="rounded-2xl border border-danger-100 bg-danger-50/80 p-4"
          >
            <div class="flex items-center justify-between">
              <div>
                <p class="text-base font-semibold text-slate-900">
                  {{ payment.student_name }}
                </p>
                <p class="text-sm text-slate-500">
                  {{ payment.group_name }}
                </p>
              </div>
              <span class="badge badge-danger uppercase">Nazorat</span>
            </div>
            <div class="mt-3 flex items-center justify-between text-sm">
              <span class="text-slate-600">Summasi</span>
              <span class="font-semibold text-danger-600">{{ formatMoney(payment.amount) }}</span>
            </div>
            <div class="mt-1 flex items-center justify-between text-xs text-slate-500">
              <span>To'lov muddati</span>
              <span>{{ formatDate(payment.due_date) }}</span>
            </div>
          </div>
          <div
            v-if="!overduePayments.length"
            class="rounded-2xl border border-dashed border-slate-200 bg-white/70 p-6 text-center text-slate-500"
          >
            Muddati o'tgan to'lovlar yo'q. Ajoyib!
          </div>
        </div>
      </div>
    </div>

    <div class="grid gap-6 lg:grid-cols-3">
      <div class="card glass-panel lg:col-span-2">
        <h3 class="text-lg font-bold text-slate-900">
          Tezkor amallar
        </h3>
        <p class="text-sm text-slate-500">
          Eng ko'p ishlatiladigan jarayonlar.
        </p>
        <div class="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
          <router-link
            to="/students"
            class="card-flat text-center"
          >
            <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500/15 to-indigo-500/20 text-primary-600">
              <UserPlusIcon class="h-7 w-7" />
            </div>
            <p class="font-medium text-slate-900">
              Yangi talaba
            </p>
            <p class="text-xs text-slate-500">
              Shartnoma tuzish
            </p>
          </router-link>
          <router-link
            to="/groups"
            class="card-flat text-center"
          >
            <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500/15 to-indigo-500/20 text-primary-600">
              <PlusCircleIcon class="h-7 w-7" />
            </div>
            <p class="font-medium text-slate-900">
              Yangi guruh
            </p>
            <p class="text-xs text-slate-500">
              Jadval yaratish
            </p>
          </router-link>
          <router-link
            to="/payments"
            class="card-flat text-center"
          >
            <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500/15 to-indigo-500/20 text-primary-600">
              <BanknotesIcon class="h-7 w-7" />
            </div>
            <p class="font-medium text-slate-900">
              To'lov qabul qil
            </p>
            <p class="text-xs text-slate-500">
              Kvitansiya
            </p>
          </router-link>
          <router-link
            to="/settings/commission"
            class="card-flat text-center"
          >
            <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500/15 to-indigo-500/20 text-primary-600">
              <Cog6ToothIcon class="h-7 w-7" />
            </div>
            <p class="font-medium text-slate-900">
              Sozlamalar
            </p>
            <p class="text-xs text-slate-500">
              Ulush va rollar
            </p>
          </router-link>
        </div>
      </div>

      <div class="card glass-panel space-y-4">
        <h3 class="text-lg font-bold text-slate-900">
          Bugungi ustuvorliklar
        </h3>
        <p class="text-sm text-slate-500">
          Kun tartibini tez ko'rib chiqing.
        </p>
        <div class="space-y-4">
          <div
            v-for="task in adminChecklist"
            :key="task.title"
            class="flex items-start gap-3 rounded-2xl border border-slate-100 bg-slate-50/50 p-4"
          >
            <div
              class="mt-1 h-3 w-3 rounded-full"
              :class="task.status === 'urgent' ? 'bg-danger-500' : 'bg-success-500'"
            />
            <div class="flex-1">
              <p class="font-semibold text-slate-900">
                {{ task.title }}
                <span class="ml-2 rounded-full bg-white px-2 py-0.5 text-xs font-medium text-slate-500">
                  {{ task.count }}
                </span>
              </p>
              <p class="text-sm text-slate-500">
                {{ task.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAnalyticsStore } from '@/store/modules/analytics'
import { usePaymentStore } from '@/store/modules/payments'
import { useStudentStore } from '@/store/modules/students'
import { useGroupStore } from '@/store/modules/groups'
import { formatDate, formatMoney } from '@/utils/helpers'
import StatCard from './StatCard.vue'
import {
  UserGroupIcon,
  AcademicCapIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  UserPlusIcon,
  PlusCircleIcon,
  BanknotesIcon,
  Cog6ToothIcon,
  ShieldCheckIcon,
} from '@heroicons/vue/24/outline'

const analyticsStore = useAnalyticsStore()
const paymentStore = usePaymentStore()
const studentStore = useStudentStore()
const groupStore = useGroupStore()

const recentEnrollments = ref([])

onMounted(async () => {
  analyticsStore.fetchRevenueSummary()
  studentStore.fetchStudents({ page_size: 5 })
  groupStore.fetchGroups({ page_size: 5 })
  paymentStore.fetchPayments({ status: 'OVERDUE', page_size: 5 })

  try {
    const data = await groupStore.fetchEnrollments({ ordering: '-enrolled_date', page_size: 5 })
    recentEnrollments.value = data
  } catch (error) {
    console.error('Enrollments fetch error', error)
  }
})

const overduePayments = computed(() => paymentStore.payments || [])

const pulseMetrics = computed(() => [
  {
    label: 'Yangi enrollments',
    value: recentEnrollments.value.length || 0,
    hint: 'Oxirgi 5 ta yozuv',
  },
  {
    label: "Muddati o'tgan",
    value: overduePayments.value.length || 0,
    hint: "Darhol ko'rib chiqing",
  },
  {
    label: "Kutilayotgan to'lov",
    value: formatMoney(analyticsStore.revenueSummary?.pending_amount || 0),
    hint: 'Tasdiqlanishi kerak',
  },
])

const adminChecklist = computed(() => [
  {
    title: "Muddati o'tgan to'lovlar",
    count: overduePayments.value.length || 0,
    description: "Talabalar bilan aloqaga chiqing va to'lovlarni tasdiqlang.",
    status: overduePayments.value.length ? 'urgent' : 'ok',
  },
  {
    title: 'Yangi enrollments',
    count: recentEnrollments.value.length || 0,
    description: 'Talaba hujjatlarini tekshiring.',
    status: recentEnrollments.value.length ? 'urgent' : 'ok',
  },
  {
    title: 'Faol guruhlar',
    count: groupStore.totalGroups || groupStore.groups.length || 0,
    description: 'Jadval va darslarda boshlanish sanalarini yangilang.',
    status: 'ok',
  },
])
</script>




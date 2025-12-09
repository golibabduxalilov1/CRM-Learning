<template>
  <div class="space-y-8">
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
            Mentor rejimi
          </div>
          <div>
            <h1 class="text-3xl font-bold tracking-tight md:text-4xl">Mentor Dashboard</h1>
            <p class="mt-2 text-sm text-white/80 max-w-2xl">
              Dars jadvali, talabalar va payoutlar ustidan to'liq nazorat. Jadvalga tayyorlaning va
              ulushingizni kuzating.
            </p>
          </div>
          <div class="flex flex-wrap gap-3">
            <span class="pill-soft">
              <ClockIcon class="h-4 w-4" />
              Jadvalga tayyor
            </span>
            <span class="pill-soft">
              <ShieldCheckIcon class="h-4 w-4" />
              OTP bilan himoya
            </span>
          </div>
        </div>

        <div
          class="glass-panel relative rounded-2xl border-white/20 bg-white/10 p-5 text-left text-white shadow-[0_20px_60px_rgba(15,23,42,0.25)] backdrop-blur"
        >
          <p class="text-xs font-semibold uppercase tracking-[0.25em] text-white/80">
            Bugungi sharh
          </p>
          <p class="mt-2 text-3xl font-extrabold">{{ mentorMetrics[0]?.value || 0 }} guruh</p>
          <p class="text-sm text-white/70">Bugungi yuklama va talabalar ro'yxati</p>
          <div class="mt-4 h-2 w-full overflow-hidden rounded-full bg-white/10">
            <div class="h-full w-2/3 rounded-full bg-gradient-to-r from-emerald-300 to-white/80" />
          </div>
        </div>
      </div>

      <div class="relative mt-6 grid gap-4 sm:grid-cols-3">
        <div
          v-for="metric in mentorMetrics"
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

    <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
      <StatCard
        title="Mening guruhlarim"
        :value="groupStore.groups.length"
        format="number"
        subtitle="Faol guruhlar soni"
        :icon="AcademicCapIcon"
      />
      <StatCard
        title="Talabalar"
        :value="totalStudents"
        format="number"
        subtitle="Faol talabalar"
        :icon="UserGroupIcon"
      />
      <StatCard
        title="Joriy oy ulushim"
        :value="currentMonthPayout"
        format="money"
        subtitle="Hisoblangan payout"
        :icon="BanknotesIcon"
        icon-bg-class="bg-green-100"
        icon-color-class="text-green-600"
      />
    </div>

    <div class="card glass-panel">
      <h3 class="text-lg font-bold text-slate-900">Payout tarixi</h3>
      <p class="text-sm text-slate-500">Hisoblangan ulushlaringizni kuzatib boring.</p>
      <div v-if="payoutStore.payouts.length" class="table-container mt-5">
        <table class="table">
          <thead>
            <tr>
              <th>Oy</th>
              <th>Yig'ilgan</th>
              <th>Mentor ulushi</th>
              <th>Status</th>
              <th>To'langan sana</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="payout in payoutStore.payouts" :key="payout.id">
              <td class="font-medium">
                {{ payout.month_display }}
              </td>
              <td>{{ formatMoney(payout.total_collected) }}</td>
              <td class="font-semibold text-green-600">
                {{ formatMoney(payout.mentor_share) }}
              </td>
              <td>
                <span :class="getStatusBadge(payout.status).class" class="badge">
                  {{ getStatusBadge(payout.status).text }}
                </span>
              </td>
              <td>{{ payout.paid_at ? formatDate(payout.paid_at) : '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div
        v-else
        class="mt-5 rounded-2xl border border-dashed border-slate-200 bg-white/70 p-6 text-center text-slate-500"
      >
        Payout tarixi hozircha mavjud emas.
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useGroupStore } from '@/store/modules/groups'
import { usePayoutStore } from '@/store/modules/payouts'
import { formatMoney, formatDate, getStatusBadge } from '@/utils/helpers'
import StatCard from './StatCard.vue'
import {
  AcademicCapIcon,
  UserGroupIcon,
  BanknotesIcon,
  ClockIcon,
  ShieldCheckIcon,
} from '@heroicons/vue/24/outline'

const groupStore = useGroupStore()
const payoutStore = usePayoutStore()

onMounted(() => {
  groupStore.fetchGroups()
  payoutStore.fetchPayouts({ page_size: 5 })
})

const totalStudents = computed(() =>
  groupStore.groups.reduce((sum, group) => sum + (group.students_count || 0), 0),
)

const currentMonthPayout = computed(() => {
  const now = new Date()
  const monthKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-01`
  const payout =
    payoutStore.payouts.find((item) => item.month === monthKey) || payoutStore.payouts[0]
  return payout ? payout.mentor_share : 0
})

const mentorMetrics = computed(() => [
  {
    label: 'Faol guruhlar',
    value: groupStore.groups.length || 0,
    hint: 'Bugungi yuklama',
  },
  {
    label: 'Talabalar',
    value: totalStudents.value || 0,
    hint: "O'quvchilar ro'yxati",
  },
  {
    label: 'Joriy oy',
    value: formatMoney(currentMonthPayout.value),
    hint: 'Hisoblangan ulush',
  },
])
</script>

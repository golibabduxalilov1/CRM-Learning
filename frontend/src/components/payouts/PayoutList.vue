<template>
  <div class="space-y-4">
    <div
      class="grid gap-4"
      :class="canManage ? 'grid-cols-1 md:grid-cols-3' : 'grid-cols-1 md:grid-cols-2'"
    >
      <select v-model="localStatus" class="input-field" @change="handleFilter">
        <option value="">Barcha statuslar</option>
        <option value="CALCULATED">Hisoblangan</option>
        <option value="PAID">To'langan</option>
        <option value="CANCELLED">Bekor qilingan</option>
      </select>
      <template v-if="canManage">
        <input
          v-model="mentorFilter"
          class="input-field"
          placeholder="Mentor ID bo'yicha filtrlash"
          type="number"
          min="1"
          @keyup.enter="handleMentorFilter"
        />
        <div class="flex gap-2">
          <button class="btn-secondary flex-1 p-2 rounded-md" @click="resetFilters">
            Filtrlarni tozalash
          </button>
          <button
            v-if="canCreate"
            class="btn-primary flex-1 p-2 rounded-md"
            @click="$emit('generate')"
          >
            Payout yaratish
          </button>
        </div>
      </template>
      <template v-else>
        <button class="btn-secondary p-2 rounded-md w-full" @click="resetFilters">
          Filtrlarni tozalash
        </button>
      </template>
    </div>

    <Loading v-if="loading" text="Payoutlar yuklanmoqda..." />

    <div v-else class="card overflow-x-auto">
      <table class="table text-center">
        <thead>
          <tr>
            <th>Mentor</th>
            <th>Oy</th>
            <th>Yig'ilgan</th>
            <th>Mentor ulushi</th>
            <th>Status</th>
            <th class="text-right">
              {{ canManage ? 'Amallar' : 'Tafsilot' }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="payout in payouts" :key="payout.id">
            <td class="font-medium">
              {{ payout.mentor_name }}
            </td>
            <td>{{ payout.month_display }}</td>
            <td>{{ formatMoney(payout.total_collected) }}</td>
            <td>{{ formatMoney(payout.mentor_share) }}</td>
            <td>
              <span :class="getStatusBadge(payout.status).class" class="badge">
                {{ getStatusBadge(payout.status).text }}
              </span>
            </td>
            <td class="text-right space-x-2">
              <button
                class="btn-secondary p-2 w-40 rounded-md mb-2"
                @click="$emit('select', payout)"
              >
                Ko'rish
              </button>
              <button
                v-if="canMark"
                class="btn-primary p-2 rounded-md"
                :disabled="payout.status === 'PAID'"
                @click="$emit('mark-paid', payout)"
              >
                To'langan deb belgilash
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="!payouts.length" class="text-center text-gray-500 py-6">Payoutlar topilmadi.</div>
    </div>

    <Pagination
      v-if="pagination.totalPages > 1"
      :current-page="pagination.currentPage"
      :total-pages="pagination.totalPages"
      :total-count="pagination.count"
      @page-change="$emit('page-change', $event)"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import Loading from '@/components/common/Loading.vue'
import Pagination from '@/components/common/Pagination.vue'
import { formatMoney, getStatusBadge } from '@/utils/helpers'

const props = defineProps({
  payouts: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  pagination: {
    type: Object,
    default: () => ({ count: 0, totalPages: 1, currentPage: 1 }),
  },
  status: {
    type: String,
    default: '',
  },
  canManage: {
    type: Boolean,
    default: true,
  },
  canCreate: {
    type: Boolean,
    default: false,
  },
  canMark: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits([
  'generate',
  'filter',
  'mentor-filter',
  'page-change',
  'mark-paid',
  'select',
])

const localStatus = ref(props.status || '')
const mentorFilter = ref('')

watch(
  () => props.status,
  (value) => {
    localStatus.value = value || ''
  },
)

const handleFilter = () => {
  emit('filter', localStatus.value)
}

const handleMentorFilter = () => {
  if (!props.canManage) return
  emit('mentor-filter', mentorFilter.value || null)
}

const resetFilters = () => {
  localStatus.value = ''
  mentorFilter.value = ''
  emit('filter', '')
  if (props.canManage) {
    emit('mentor-filter', null)
  }
}
</script>

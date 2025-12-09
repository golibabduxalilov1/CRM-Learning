<template>
  <div class="space-y-4">
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
      <input
        v-model="localSearch"
        type="text"
        class="input-field"
        placeholder="Talaba, guruh yoki summa bo'yicha qidiring"
        @keyup.enter="handleSearch"
      />
      <select v-model="selectedStatus" class="input-field" @change="handleFilter">
        <option value="">Barcha holatlar</option>
        <option v-for="option in statusOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>
      <button class="btn-secondary p-2 rounded-md" @click="handleReset">Filtrlarni tozalash</button>
      <button class="btn-primary p-2 rounded-md" @click="$emit('create')">Yangi to'lov</button>
    </div>

    <Loading v-if="loading" text="To'lovlar yuklanmoqda..." />

    <div v-else class="card overflow-x-auto">
      <table class="table">
        <thead>
          <tr>
            <th>Talaba</th>
            <th>Guruh</th>
            <th>Miqdor</th>
            <th>Holat</th>
            <th>Muddati</th>
            <th class="text-right">Amallar</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="payment in payments" :key="payment.id">
            <td class="font-medium">
              {{ payment.student_name }}
            </td>
            <td>{{ payment.group_name }}</td>
            <td>{{ formatMoney(payment.amount) }}</td>
            <td>
              <span :class="getStatusBadge(payment.status).class" class="badge">
                {{ getStatusBadge(payment.status).text }}
              </span>
            </td>
            <td>{{ formatDate(payment.due_date) }}</td>
            <td class="text-right space-x-2">
              <button
                class="btn-secondary px-3 py-1 p-2 rounded-md"
                @click="$emit('edit', payment)"
              >
                Tahrirlash
              </button>
              <button
                class="btn-secondary px-3 py-1 p-2 rounded-md"
                @click="$emit('status', payment)"
              >
                Holat
              </button>
              <button
                class="btn-danger px-3 py-1 p-2 rounded-md"
                @click="$emit('delete', payment.id)"
              >
                O'chirish
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="!payments.length" class="text-center text-gray-500 py-6">To'lovlar topilmadi.</div>
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
import { formatDate, formatMoney, getStatusBadge } from '@/utils/helpers'

const props = defineProps({
  payments: {
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
  search: {
    type: String,
    default: '',
  },
  status: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['create', 'search', 'filter', 'page-change', 'status', 'edit', 'delete'])

const localSearch = ref(props.search || '')
const selectedStatus = ref(props.status || '')

watch(
  () => props.search,
  (value) => {
    localSearch.value = value || ''
  },
)

watch(
  () => props.status,
  (value) => {
    selectedStatus.value = value || ''
  },
)

const statusOptions = [
  { value: 'PENDING', label: 'Kutilmoqda' },
  { value: 'PAID', label: "To'langan" },
  { value: 'OVERDUE', label: "Muddati o'tgan" },
  { value: 'CANCELLED', label: 'Bekor qilingan' },
]

const handleSearch = () => {
  emit('search', localSearch.value.trim())
}

const handleFilter = () => {
  emit('filter', selectedStatus.value)
}

const handleReset = () => {
  localSearch.value = ''
  selectedStatus.value = ''
  emit('search', '')
  emit('filter', '')
}
</script>

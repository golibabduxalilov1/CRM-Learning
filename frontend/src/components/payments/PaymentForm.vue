<template>
  <form
    class="space-y-4"
    @submit.prevent="handleSubmit"
  >
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Talaba</label>
        <select
          v-model="form.student"
          class="input-field"
          required
        >
          <option value="">
            Talabani tanlang
          </option>
          <option
            v-for="student in students"
            :key="student.id"
            :value="student.id"
          >
            {{ student.first_name }} {{ student.last_name }}
          </option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Guruh</label>
        <select
          v-model="form.group"
          class="input-field"
          required
        >
          <option value="">
            Guruhni tanlang
          </option>
          <option
            v-for="group in groups"
            :key="group.id"
            :value="group.id"
          >
            {{ group.name }}
          </option>
        </select>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Miqdor</label>
        <input
          v-model.number="form.amount"
          type="number"
          min="0"
          step="50000"
          class="input-field"
          required
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Muddati</label>
        <input
          v-model="form.due_date"
          type="date"
          class="input-field"
          required
        >
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Holat</label>
        <select
          v-model="form.status"
          class="input-field"
        >
          <option value="PENDING">
            Kutilmoqda
          </option>
          <option value="PAID">
            To'langan
          </option>
          <option value="OVERDUE">
            Muddati o'tgan
          </option>
          <option value="CANCELLED">
            Bekor qilingan
          </option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">To'lov usuli</label>
        <input
          v-model="form.payment_method"
          type="text"
          class="input-field"
          placeholder="Naqd, karta va hokazo"
        >
      </div>
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Izoh</label>
      <textarea
        v-model="form.notes"
        rows="3"
        class="input-field"
        placeholder="Ixtiyoriy"
      />
    </div>

    <div class="flex items-center justify-end gap-3">
      <button
        type="button"
        class="btn-secondary p-2 rounded-md"
        :disabled="loading"
        @click="emit('cancel')"
      >
        Bekor qilish
      </button>
      <button
        type="submit"
        class="btn-primary p-2 rounded-md"
        :disabled="loading"
      >
        {{ loading ? 'Saqlanmoqda...' : isEdit ? 'Yangilash' : "To'lov yaratish" }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { computed, reactive, watch } from 'vue'

const props = defineProps({
  payment: {
    type: Object,
    default: null,
  },
  students: {
    type: Array,
    default: () => [],
  },
  groups: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive(getInitialForm(props.payment))

watch(
  () => props.payment,
  (value) => {
    Object.assign(form, getInitialForm(value))
  },
  { immediate: true }
)

const isEdit = computed(() => Boolean(props.payment?.id))

const handleSubmit = () => {
  emit('submit', {
    ...form,
    amount: Number(form.amount),
  })
}

function getInitialForm(payment) {
  return {
    student: payment?.student || '',
    group: payment?.group || '',
    amount: payment?.amount || 0,
    due_date: payment?.due_date || '',
    status: payment?.status || 'PENDING',
    payment_method: payment?.payment_method || '',
    notes: payment?.notes || '',
  }
}
</script>

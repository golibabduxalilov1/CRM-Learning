<template>
  <Modal
    :show="show"
    title="To'lov holatini yangilash"
    @close="emit('close')"
  >
    <form
      class="space-y-4"
      @submit.prevent="handleSubmit"
    >
      <div>
        <p class="text-sm text-gray-500">
          Talaba
        </p>
        <p class="font-semibold text-gray-900">
          {{ payment?.student_name }}
        </p>
      </div>

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

      <div v-if="form.status === 'PAID'">
        <label class="block text-sm font-medium text-gray-700 mb-1">To'lov usuli</label>
        <input
          v-model="form.payment_method"
          type="text"
          class="input-field"
          placeholder="Naqd, karta va hokazo"
        >
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

      <div class="flex justify-end gap-3">
        <button
          type="button"
          class="btn-secondary p-2 rounded-md"
          @click="emit('close')"
        >
          Bekor qilish
        </button>
        <button
          type="submit"
          class="btn-primary p-2 rounded-md"
          :disabled="loading"
        >
          {{ loading ? 'Saqlanmoqda...' : 'Holatni yangilash' }}
        </button>
      </div>
    </form>
  </Modal>
</template>

<script setup>
import { reactive, watch } from 'vue'
import Modal from '@/components/common/Modal.vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  payment: {
    type: Object,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update', 'close'])

const form = reactive({
  status: 'PENDING',
  payment_method: '',
  notes: '',
})

watch(
  () => props.payment,
  (payment) => {
    form.status = payment?.status || 'PENDING'
    form.payment_method = payment?.payment_method || ''
    form.notes = payment?.notes || ''
  },
  { immediate: true }
)

const handleSubmit = () => {
  emit('update', {
    status: form.status,
    payment_method: form.payment_method,
    notes: form.notes,
  })
}
</script>

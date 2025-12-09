<template>
  <Modal
    :show="show"
    title="Yangi payout yaratish"
    @close="emit('close')"
  >
    <form
      class="space-y-4"
      @submit.prevent="handleSubmit"
    >
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Mentor</label>
        <select
          v-model="form.mentor_id"
          class="input-field"
          required
        >
          <option value="">
            Mentorni tanlang
          </option>
          <option
            v-for="mentor in mentors"
            :key="mentor.id"
            :value="mentor.id"
          >
            {{ mentor.first_name }} {{ mentor.last_name }}
          </option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Oy (YYYY-MM)</label>
        <input
          v-model="form.month"
          type="month"
          class="input-field"
          required
        >
      </div>

      <div class="flex justify-end gap-3">
        <button
          type="button"
          class="btn-secondary p-2 rounded-md"
          :disabled="loading"
          @click="emit('close')"
        >
          Bekor qilish
        </button>
        <button
          type="submit"
          class="btn-primary p-2 rounded-md"
          :disabled="loading"
        >
          {{ loading ? 'Hisoblanmoqda...' : 'Payout yaratish' }}
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
  mentors: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['generate', 'close'])

const form = reactive({
  mentor_id: '',
  month: '',
})

watch(
  () => props.show,
  (visible) => {
    if (!visible) {
      form.mentor_id = ''
      form.month = ''
    }
  }
)

const handleSubmit = () => {
  emit('generate', {
    mentor_id: form.mentor_id,
    month: form.month,
  })
}
</script>

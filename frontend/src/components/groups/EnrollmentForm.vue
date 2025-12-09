<template>
  <form
    class="space-y-4"
    @submit.prevent="handleSubmit"
  >
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
          {{ student.first_name }} {{ student.last_name }} — {{ student.email }}
        </option>
      </select>
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Holat</label>
      <select
        v-model="form.status"
        class="input-field"
      >
        <option
          v-for="status in statusOptions"
          :key="status.value"
          :value="status.value"
        >
          {{ status.label }}
        </option>
      </select>
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
        {{ loading ? 'Yuklanmoqda...' : 'Talabani qo\'shish' }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { computed, reactive, watch } from 'vue'
import { ENROLLMENT_STATUS } from '@/utils/constants'

const props = defineProps({
  groupId: {
    type: Number,
    required: true,
  },
  students: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({
  student: '',
  status: ENROLLMENT_STATUS.ACTIVE,
})

watch(
  () => props.groupId,
  () => {
    form.student = ''
    form.status = ENROLLMENT_STATUS.ACTIVE
  }
)

const formatStatusLabel = (value) => {
  const labels = {
    ACTIVE: 'Faol',
    PAUSED: "To'xtatilgan",
    COMPLETED: 'Tugatilgan',
    DROPPED: 'Tashlab ketgan',
  }
  return labels[value] || value
}

const statusOptions = computed(() =>
  Object.entries(ENROLLMENT_STATUS).map(([value]) => ({
    value,
    label: formatStatusLabel(value),
  }))
)

const handleSubmit = () => {
  emit('submit', {
    student: form.student,
    group: props.groupId,
    status: form.status,
  })
}
</script>

<template>
  <form class="space-y-4" @submit.prevent="emit('submit')">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Mentor ulushi (%)</label>
        <input
          :value="modelValue.mentor_percentage"
          type="number"
          min="0"
          max="100"
          step="1"
          class="input-field"
          @input="updateField('mentor_percentage', $event.target.valueAsNumber)"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Markaz ulushi (%)</label>
        <input
          :value="modelValue.center_percentage"
          type="number"
          min="0"
          max="100"
          step="1"
          class="input-field"
          @input="updateField('center_percentage', $event.target.valueAsNumber)"
        />
      </div>
    </div>

    <div class="flex items-center gap-2">
      <input
        id="is_active"
        :checked="modelValue.is_active"
        type="checkbox"
        class="h-4 w-4 text-primary-600"
        @change="updateField('is_active', $event.target.checked)"
      />
      <label for="is_active" class="text-sm text-gray-700">Sozlama faol</label>
    </div>

    <div class="flex items-center justify-between text-sm text-gray-500">
      <span>Oxirgi yangilanish: {{ updatedAt ? formatDate(updatedAt) : '-' }}</span>
    </div>

    <button type="submit" class="btn-primary p-2 rounded-md" :disabled="loading">
      {{ loading ? 'Saqlanmoqda...' : 'Saqlash' }}
    </button>
  </form>
</template>

<script setup>
import { formatDate } from '@/utils/helpers'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  updatedAt: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue', 'submit'])

const updateField = (field, value) => {
  const parsedValue =
    typeof value === 'number' && Number.isNaN(value) ? props.modelValue[field] : value
  emit('update:modelValue', {
    ...props.modelValue,
    [field]: parsedValue,
  })
}
</script>

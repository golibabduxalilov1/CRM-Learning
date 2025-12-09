<template>
  <div class="card">
    <p class="text-sm text-gray-500">
      {{ label }}
    </p>
    <p class="text-2xl font-bold text-gray-900 mt-1">
      {{ formattedValue }}
    </p>
    <p
      v-if="description"
      class="text-xs text-gray-500 mt-1"
    >
      {{ description }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatMoney } from '@/utils/helpers'

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: [Number, String],
    default: 0,
  },
  format: {
    type: String,
    default: 'money',
  },
  description: {
    type: String,
    default: '',
  },
})

const formattedValue = computed(() => {
  if (props.format === 'money') {
    return formatMoney(props.value)
  }
  return new Intl.NumberFormat('uz-UZ').format(props.value || 0)
})
</script>

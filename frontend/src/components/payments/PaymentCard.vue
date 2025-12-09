<template>
  <div class="card flex flex-col gap-2">
    <div class="flex items-center justify-between">
      <p class="text-sm text-gray-500">
        {{ label }}
      </p>
      <component
        :is="icon"
        v-if="icon"
        class="w-5 h-5 text-primary-500"
      />
    </div>
    <p class="text-2xl font-bold text-gray-900">
      {{ formattedValue }}
    </p>
    <p
      v-if="description"
      class="text-xs text-gray-500"
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
    default: 'number',
  },
  description: {
    type: String,
    default: '',
  },
  icon: {
    type: [Object, Function],
    default: null,
  },
})

const formattedValue = computed(() => {
  if (props.format === 'money') {
    return formatMoney(props.value)
  }
  if (props.format === 'text') {
    return props.value
  }
  return new Intl.NumberFormat('uz-UZ').format(props.value || 0)
})
</script>

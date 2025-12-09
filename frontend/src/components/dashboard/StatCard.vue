<template>
  <div class="card hover:scale-105 transition-transform duration-300">
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <p class="text-sm font-medium text-gray-600 mb-1">
          {{ title }}
        </p>
        <p class="text-3xl font-bold text-gray-900">
          {{ formattedValue }}
        </p>
        <p
          v-if="subtitle"
          class="text-sm text-gray-500 mt-2"
        >
          {{ subtitle }}
        </p>
      </div>
      <div
        class="w-12 h-12 rounded-lg flex items-center justify-center"
        :class="iconBgClass"
      >
        <component
          :is="icon"
          class="w-7 h-7"
          :class="iconColorClass"
        />
      </div>
    </div>

    <div
      v-if="trend"
      class="mt-4 flex items-center text-sm"
    >
      <component
        :is="trend > 0 ? ArrowUpIcon : ArrowDownIcon"
        class="w-4 h-4 mr-1"
        :class="trend > 0 ? 'text-success-600' : 'text-danger-600'"
      />
      <span :class="trend > 0 ? 'text-success-600' : 'text-danger-600'">
        {{ Math.abs(trend) }}%
      </span>
      <span class="text-gray-600 ml-1">o'tgan oyga nisbatan</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/vue/24/solid'
import { formatMoney } from '@/utils/helpers'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
  icon: {
    type: [Object, Function],
    required: true,
  },
  iconBgClass: {
    type: String,
    default: 'bg-primary-100',
  },
  iconColorClass: {
    type: String,
    default: 'text-primary-600',
  },
  trend: {
    type: Number,
    default: null,
  },
  format: {
    type: String,
    default: 'number',
    validator: (value) => ['number', 'money', 'text'].includes(value),
  },
})

const formattedValue = computed(() => {
  if (props.format === 'money') {
    return formatMoney(props.value)
  } else if (props.format === 'number') {
    return new Intl.NumberFormat('uz-UZ').format(props.value)
  }
  return props.value
})
</script>

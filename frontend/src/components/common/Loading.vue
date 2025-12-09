<template>
  <div
    class="flex items-center justify-center"
    :class="containerClass"
  >
    <div class="relative">
      <div
        class="animate-spin rounded-full border-b-2"
        :class="[sizeClass, colorClass]"
      />
      <div
        v-if="text"
        class="mt-4 text-center text-sm font-medium text-gray-600"
      >
        {{ text }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg', 'xl'].includes(v),
  },
  color: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'white', 'gray'].includes(v),
  },
  text: {
    type: String,
    default: '',
  },
  fullscreen: {
    type: Boolean,
    default: false,
  },
})

const sizeClass = computed(() => {
  const sizes = {
    sm: 'h-6 w-6',
    md: 'h-12 w-12',
    lg: 'h-16 w-16',
    xl: 'h-24 w-24',
  }
  return sizes[props.size]
})

const colorClass = computed(() => {
  const colors = {
    primary: 'border-primary-600',
    white: 'border-white',
    gray: 'border-gray-600',
  }
  return colors[props.color]
})

const containerClass = computed(() => {
  return props.fullscreen ? 'min-h-screen' : 'h-64'
})
</script>

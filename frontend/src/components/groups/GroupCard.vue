<template>
  <div class="card hover:scale-105 transition-transform cursor-pointer" @click="$emit('click')">
    <div class="flex items-start justify-between mb-3">
      <h3 class="font-bold text-gray-900 text-lg">
        {{ group.name }}
      </h3>
      <span :class="getCapacityBadge()" class="badge">
        {{ studentCount }}/{{ group.max_students }}
      </span>
    </div>

    <p class="text-sm text-gray-600 mb-4">
      {{ group.subject }}
    </p>

    <div class="space-y-2 text-sm mb-4">
      <div class="flex justify-between">
        <span class="text-gray-600">Mentor:</span>
        <span class="font-medium">{{ group.mentor_name || 'Tayinlanmagan' }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-600">Narx:</span>
        <span class="font-medium text-primary-600">{{ formatMoney(group.price_per_month) }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-600">Davr:</span>
        <span class="font-medium">{{ formatDate(group.start_date) }}</span>
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="mb-4">
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div
          class="h-2 rounded-full transition-all"
          :class="getProgressBarClass()"
          :style="{ width: `${getCapacityPercentage()}%` }"
        />
      </div>
    </div>

    <div v-if="canManage" class="flex space-x-2">
      <button
        class="flex-1 text-sm text-green-600 hover:bg-green-50 py-2 transition-colors p-2 rounded-md"
        @click.stop="$emit('edit', group)"
      >
        Tahrirlash
      </button>
      <button
        class="flex-1 text-sm text-primary-600 hover:bg-primary-50 py-2 transition-colors p-2 rounded-md"
        @click.stop="$emit('assign-mentor', group.id)"
      >
        Mentor
      </button>
      <button
        class="flex-1 text-sm text-danger-600 hover:bg-danger-50 py-2 transition-colors p-2 rounded-md"
        @click.stop="$emit('delete', group.id)"
      >
        O'chirish
      </button>
    </div>
  </div>
</template>

<script setup>
import { formatMoney, formatDate } from '@/utils/helpers'

import { computed } from 'vue'

const props = defineProps({
  group: {
    type: Object,
    required: true,
  },
  canManage: {
    type: Boolean,
    default: true,
  },
})

defineEmits(['click', 'edit', 'assign-mentor', 'delete'])

const studentCount = computed(() => props.group.students_count ?? props.group.students?.length ?? 0)

const getCapacityPercentage = () => {
  if (!props.group.max_students) return 0
  return Math.min(100, (studentCount.value / props.group.max_students) * 100)
}

const getCapacityBadge = () => {
  const percentage = getCapacityPercentage()
  if (percentage >= 90) return 'badge-danger'
  if (percentage >= 70) return 'badge-warning'
  return 'badge-success'
}

const getProgressBarClass = () => {
  const percentage = getCapacityPercentage()
  if (percentage >= 90) return 'bg-red-500'
  if (percentage >= 70) return 'bg-yellow-500'
  return 'bg-green-500'
}
</script>

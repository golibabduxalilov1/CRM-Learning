<template>
  <div
    class="card hover:scale-105 transition-transform cursor-pointer"
    @click="$emit('click')"
  >
    <div class="flex items-start justify-between mb-4">
      <div class="flex items-center space-x-3">
        <div class="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
          <span class="text-primary-700 font-bold text-lg">
            {{ student.first_name[0] }}{{ student.last_name[0] }}
          </span>
        </div>
        <div>
          <h3 class="font-bold text-gray-900">
            {{ student.first_name }} {{ student.last_name }}
          </h3>
          <p class="text-sm text-gray-600">
            {{ student.email }}
          </p>
        </div>
      </div>
      <span class="badge badge-success">Faol</span>
    </div>

    <div class="space-y-2 text-sm">
      <div class="flex justify-between">
        <span class="text-gray-600">Telefon:</span>
        <span class="font-medium">{{ student.phone }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-600">Guruhlar:</span>
        <span class="font-medium">{{ student.enrollments_count }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-gray-600">Qo'shilgan:</span>
        <span class="font-medium">{{ formatDate(student.created_at) }}</span>
      </div>
    </div>

    <div class="mt-4 pt-4 border-t border-gray-200 flex space-x-2">
      <button
        class="flex-1 text-sm text-green-600 hover:bg-green-50 py-2 rounded-lg transition-colors p-2 rounded-md"
        @click.stop="$emit('edit', student)"
      >
        Tahrirlash
      </button>
      <button
        class="flex-1 text-sm text-red-600 hover:bg-red-50 py-2 rounded-lg transition-colors p-2 rounded-md"
        @click.stop="$emit('delete', student.id)"
      >
        O'chirish
      </button>
    </div>
  </div>
</template>

<script setup>
import { formatDate } from '@/utils/helpers'

defineProps({
  student: {
    type: Object,
    required: true,
  },
})

defineEmits(['click', 'edit', 'delete'])
</script>

<template>
  <div
    v-if="totalPages > 1"
    class="flex items-center justify-between px-4 py-3 bg-white border-t border-gray-200 sm:px-6"
  >
    <div class="flex items-center justify-between flex-1 sm:hidden">
      <button
        :disabled="currentPage === 1"
        class="btn-secondary p-2 rounded-md"
        @click="emit('page-change', currentPage - 1)"
      >
        Oldingi
      </button>
      <span class="text-sm text-gray-700">
        Sahifa {{ currentPage }} / {{ totalPages }}
      </span>
      <button
        :disabled="currentPage === totalPages"
        class="btn-secondary p-2 rounded-md"
        @click="emit('page-change', currentPage + 1)"
      >
        Keyingi
      </button>
    </div>

    <div class="hidden sm:flex sm:items-center sm:justify-between w-full">
      <div>
        <p class="text-sm text-gray-700">
          Jami <span class="font-medium">{{ totalCount }}</span> ta natija
        </p>
      </div>
      <div class="flex space-x-2">
        <button
          :disabled="currentPage === 1"
          class="px-3 py-1 rounded border p-2 rounded-md"
          :class="
            currentPage === 1
              ? 'bg-gray-100 cursor-not-allowed'
              : 'hover:bg-gray-100'
          "
          @click="emit('page-change', 1)"
        >
          Birinchi
        </button>

        <button
          :disabled="currentPage === 1"
          class="px-3 py-1 rounded border p-2 rounded-md"
          :class="
            currentPage === 1
              ? 'bg-gray-100 cursor-not-allowed'
              : 'hover:bg-gray-100'
          "
          @click="emit('page-change', currentPage - 1)"
        >
          &lt;
        </button>

        <template
          v-for="page in visiblePages"
          :key="`page-${page}`"
        >
          <button
            v-if="page !== '...'"
            class="px-3 py-1 rounded border p-2 rounded-md"
            :class="
              page === currentPage
                ? 'bg-primary-600 text-white'
                : 'hover:bg-gray-100'
            "
            @click="emit('page-change', page)"
          >
            {{ page }}
          </button>
          <span
            v-else
            class="px-3 py-1 text-gray-400 select-none"
          >...</span>
        </template>

        <button
          :disabled="currentPage === totalPages"
          class="px-3 py-1 rounded border p-2 rounded-md"
          :class="
            currentPage === totalPages
              ? 'bg-gray-100 cursor-not-allowed'
              : 'hover:bg-gray-100'
          "
          @click="emit('page-change', currentPage + 1)"
        >
          &gt;
        </button>
        <button
          :disabled="currentPage === totalPages"
          class="px-3 py-1 rounded border p-2 rounded-md"
          :class="
            currentPage === totalPages
              ? 'bg-gray-100 cursor-not-allowed'
              : 'hover:bg-gray-100'
          "
          @click="emit('page-change', totalPages)"
        >
          Oxirgi
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
  totalCount: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(['page-change'])

const visiblePages = computed(() => {
  const delta = 2
  const range = []
  const rangeWithDots = []
  let previous

  for (let i = 1; i <= props.totalPages; i += 1) {
    if (
      i === 1 ||
      i === props.totalPages ||
      (i >= props.currentPage - delta && i <= props.currentPage + delta)
    ) {
      range.push(i)
    }
  }

  range.forEach((page) => {
    if (previous) {
      if (page - previous === 2) {
        rangeWithDots.push(previous + 1)
      } else if (page - previous > 2) {
        rangeWithDots.push('...')
      }
    }
    rangeWithDots.push(page)
    previous = page
  })

  return rangeWithDots
})
</script>

<template>
  <teleport to="body">
    <transition name="slide">
      <div
        v-if="show"
        class="fixed top-4 right-4 z-50 max-w-sm w-full"
      >
        <div
          class="rounded-2xl shadow-glass border p-4 backdrop-blur-xl"
          :class="typeClasses"
        >
          <div class="flex items-start">
            <component
              :is="icon"
              class="h-6 w-6 flex-shrink-0"
            />

            <div class="ml-3 flex-1">
              <p class="text-sm font-bold">
                {{ title }}
              </p>
              <p class="mt-1 text-sm opacity-90">
                {{ message }}
              </p>
            </div>

            <button
              class="ml-4 flex-shrink-0 hover:opacity-75 transition-opacity p-2 rounded-md"
              @click="$emit('close')"
            >
              <XMarkIcon class="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { computed, watch } from 'vue'
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  InformationCircleIcon,
  ExclamationTriangleIcon,
  XMarkIcon,
} from '@heroicons/vue/24/solid'

const props = defineProps({
  show: Boolean,
  type: {
    type: String,
    default: 'info',
    validator: (v) => ['success', 'error', 'warning', 'info'].includes(v),
  },
  title: String,
  message: String,
  duration: {
    type: Number,
    default: 3000,
  },
})

const emit = defineEmits(['close'])

/* ---------- presentation helpers ---------- */
const typeClasses = computed(
  () =>
    ({
      success: 'bg-emerald-50/90 border-emerald-200 text-emerald-800',
      error: 'bg-rose-50/90 border-rose-200 text-rose-800',
      warning: 'bg-amber-50/90 border-amber-200 text-amber-800',
      info: 'bg-blue-50/90 border-blue-200 text-blue-800',
    })[props.type]
)

const icon = computed(
  () =>
    ({
      success: CheckCircleIcon,
      error: ExclamationCircleIcon,
      warning: ExclamationTriangleIcon,
      info: InformationCircleIcon,
    })[props.type]
)

/* ---------- auto-dismiss ---------- */
let timer
watch(
  () => props.show,
  (visible) => {
    if (visible && props.duration > 0) {
      clearTimeout(timer)
      timer = setTimeout(() => emit('close'), props.duration)
    } else {
      clearTimeout(timer)
    }
  }
)
</script>

<style scoped>
.slide-enter-active {
  transition: all 0.3s ease-out;
}
.slide-leave-active {
  transition: all 0.2s ease-in;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>

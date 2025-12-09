<template>
  <div
    v-if="payout"
    class="card space-y-3"
  >
    <div>
      <p class="text-sm text-gray-500">
        Mentor
      </p>
      <p class="font-semibold text-gray-900">
        {{ payout.mentor_name }}
      </p>
    </div>
    <div class="grid grid-cols-2 gap-4 text-sm text-gray-600">
      <div>
        <p class="text-gray-500">
          Oy
        </p>
        <p class="font-semibold text-gray-900">
          {{ payout.month_display }}
        </p>
      </div>
      <div>
        <p class="text-gray-500">
          Status
        </p>
        <span
          :class="getStatusBadge(payout.status).class"
          class="badge"
        >
          {{ getStatusBadge(payout.status).text }}
        </span>
      </div>
      <div>
        <p class="text-gray-500">
          Jami yig'ilgan
        </p>
        <p class="font-semibold text-gray-900">
          {{ formatMoney(payout.total_collected) }}
        </p>
      </div>
      <div>
        <p class="text-gray-500">
          Mentor ulushi
        </p>
        <p class="font-semibold text-green-600">
          {{ formatMoney(payout.mentor_share) }}
        </p>
      </div>
    </div>
    <div
      v-if="hasPaymentDetails"
      class="text-sm text-gray-600"
    >
      <p class="text-gray-500">
        To'lov ma'lumotlari
      </p>
      <pre class="bg-gray-50 rounded-lg p-3 mt-1 text-xs overflow-auto">{{ formattedPaymentDetails }}</pre>
    </div>
  </div>
  <div
    v-else
    class="card text-center text-gray-500"
  >
    Payout tanlanmagan.
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { formatMoney, getStatusBadge } from '@/utils/helpers'

const props = defineProps({
  payout: {
    type: Object,
    default: null,
  },
})

const hasPaymentDetails = computed(
  () => props.payout && props.payout.payment_details && Object.keys(props.payout.payment_details).length > 0
)

const formattedPaymentDetails = computed(() =>
  hasPaymentDetails.value ? JSON.stringify(props.payout.payment_details, null, 2) : ''
)
</script>

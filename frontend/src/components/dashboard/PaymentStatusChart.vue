<template>
  <div class="card">
    <h3 class="text-lg font-bold mb-4">
      To'lov holati
    </h3>
    <div class="h-64">
      <Doughnut
        :data="chartData"
        :options="chartOptions"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
})

const chartData = computed(() => ({
  labels: props.data.map((item) => {
    const labels = {
      PAID: "To'langan",
      PENDING: 'Kutilmoqda',
      OVERDUE: "Muddati o'tgan",
      CANCELLED: 'Bekor qilingan',
    }
    return labels[item.status] || item.status
  }),
  datasets: [
    {
      data: props.data.map((item) => item.count),
      backgroundColor: ['#22c55e', '#f59e0b', '#ef4444', '#6b7280'],
      borderWidth: 2,
      borderColor: '#fff',
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const label = context.label || ''
          const value = context.parsed
          return `${label}: ${value} ta`
        },
      },
    },
  },
}
</script>

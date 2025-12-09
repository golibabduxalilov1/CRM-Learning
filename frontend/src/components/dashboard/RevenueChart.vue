<template>
  <div class="card p-4">
    <div class="flex items-center justify-between mb-4">
      <div>
        <h3 class="text-lg font-bold text-slate-900">Oylik daromad</h3>
        <p class="text-sm text-slate-500">Oxirgi oylar bo'yicha tushum grafigi</p>
      </div>
    </div>
    <div class="h-64">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import dayjs from 'dayjs'
import 'dayjs/locale/uz'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
)

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
})

const formattedData = computed(() =>
  (props.data || []).map((item) => ({
    label: dayjs(item.month).locale('uz').format('MMM YYYY'),
    revenue: Number(item.revenue) || 0,
    count: Number(item.count) || 0,
  })),
)

const chartData = computed(() => ({
  labels: formattedData.value.map((item) => item.label),
  datasets: [
    {
      label: "Daromad (so'm)",
      data: formattedData.value.map((item) => item.revenue),
      borderColor: '#2563eb',
      backgroundColor: 'rgba(37, 99, 235, 0.12)',
      fill: true,
      tension: 0.4,
      pointRadius: 4,
      pointHoverRadius: 6,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: {
      display: true,
      position: 'bottom',
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const value = context.parsed.y || 0
          return `${context.dataset.label}: ${new Intl.NumberFormat('uz-UZ').format(value)} so'm`
        },
      },
    },
  },
  scales: {
    x: {
      display: true,
      ticks: {
        maxRotation: 0,
      },
    },
    y: {
      beginAtZero: true,
      ticks: {
        callback: (value) => {
          return new Intl.NumberFormat('uz-UZ', {
            notation: 'compact',
            compactDisplay: 'short',
          }).format(value)
        },
      },
    },
  },
}
</script>

<template>
  <div class="flex bg-gray-50 min-h-screen">
    <Sidebar />
    <div class="flex-1">
      <Navbar />
      <div class="p-6 space-y-6">
        <h1 class="text-3xl font-bold text-gray-900">Komissiya sozlamalari</h1>
        <p class="text-gray-500">Global mentor va markaz ulushlari.</p>

        <div class="card">
          <CommissionForm
            :model-value="form"
            :loading="paymentStore.loading"
            :updated-at="paymentStore.commissionSettings?.updated_at"
            @update:model-value="updateForm"
            @submit="handleSave"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch, onMounted } from 'vue'
import Sidebar from '@/components/common/Sidebar.vue'
import Navbar from '@/components/common/Navbar.vue'
import CommissionForm from '@/components/settings/CommissionForm.vue'
import { usePaymentStore } from '@/store/modules/payments'
import { useNotification } from '@/composables/useNotification'

const paymentStore = usePaymentStore()
const { showSuccess, showError } = useNotification()

const form = reactive({
  mentor_percentage: 60,
  center_percentage: 40,
  is_active: true,
})

onMounted(async () => {
  await paymentStore.fetchCommissionSettings()
  if (paymentStore.commissionSettings) {
    Object.assign(form, {
      mentor_percentage: Number(paymentStore.commissionSettings.mentor_percentage),
      center_percentage: Number(paymentStore.commissionSettings.center_percentage),
      is_active: paymentStore.commissionSettings.is_active,
    })
  }
})

watch(
  () => paymentStore.commissionSettings,
  (settings) => {
    if (settings) {
      Object.assign(form, {
        mentor_percentage: Number(settings.mentor_percentage),
        center_percentage: Number(settings.center_percentage),
        is_active: settings.is_active,
      })
    }
  },
)

const handleSave = async () => {
  const total = Number(form.mentor_percentage) + Number(form.center_percentage)
  if (total !== 100) {
    showError("Foizlar yig'indisi 100 bo'lishi kerak")
    return
  }

  const result = await paymentStore.updateCommissionSettings(form)
  if (result.success) {
    showSuccess('Komissiya sozlamalari yangilandi')
  } else {
    showError(result.error?.detail || 'Saqlashda xatolik')
  }
}

const updateForm = (value) => {
  Object.assign(form, value)
}
</script>

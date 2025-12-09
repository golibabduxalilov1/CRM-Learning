<template>
  <div class="flex min-h-screen bg-slate-50">
    <Sidebar />
    <div class="flex-1 flex flex-col min-w-0">
      <Navbar />
      <main class="flex-1 px-4 py-8 lg:px-8 space-y-8">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 class="text-2xl font-bold text-slate-800 flex items-center gap-2">
              <span class="w-1.5 h-7 rounded-full bg-primary-500"></span>
              Mentor payoutlari
            </h1>
            <p class="text-sm text-slate-500 ml-3.5 mt-1">Hisoblangan va to'langan ulushlar</p>
          </div>
          <button
            v-if="canCreatePayouts"
            class="btn-primary p-2 rounded-md"
            @click="showGenerateModal = true"
          >
            Payout yaratish
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <PayoutCard
            label="Hisoblangan"
            :value="payoutStore.totalCalculated"
            description="To'lanishga tayyor"
          />
          <PayoutCard
            label="To'langan"
            :value="payoutStore.totalPaid"
            description="Yakunlangan to'lovlar"
          />
          <PayoutCard
            label="Jami payoutlar"
            :value="payoutStore.pagination.count"
            format="number"
            description="Yozuvlar soni"
          />
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2">
            <PayoutList
              :payouts="payoutStore.payouts"
              :loading="payoutStore.loading"
              :pagination="payoutStore.pagination"
              :status="statusFilter"
              :can-manage="canManagePayouts"
              :can-create="canCreatePayouts"
              :can-mark="canMarkPayouts"
              @generate="showGenerateModal = true"
              @filter="handleStatusFilter"
              @mentor-filter="handleMentorFilter"
              @page-change="handlePageChange"
              @mark-paid="prepareMarkPaid"
              @select="selectedPayout = $event"
            />
          </div>
          <PayoutDetail :payout="selectedPayout" />
        </div>
      </main>
    </div>
  </div>

  <GeneratePayoutModal
    v-if="canCreatePayouts"
    :show="showGenerateModal"
    :mentors="groupStore.mentors"
    :loading="payoutStore.loading"
    @close="showGenerateModal = false"
    @generate="handleGeneratePayout"
  />

  <ConfirmDialog
    v-if="canMarkPayouts"
    :show="showMarkPaidDialog"
    title="Payoutni tasdiqlash"
    message="Ushbu payoutni to'langan deb belgilashni tasdiqlaysizmi?"
    confirm-text="Ha, tasdiqlayman"
    cancel-text="Bekor qilish"
    @confirm="confirmMarkPaid"
    @cancel="showMarkPaidDialog = false"
  />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import Sidebar from '@/components/common/Sidebar.vue'
import Navbar from '@/components/common/Navbar.vue'
import PayoutList from '@/components/payouts/PayoutList.vue'
import PayoutCard from '@/components/payouts/PayoutCard.vue'
import PayoutDetail from '@/components/payouts/PayoutDetail.vue'
import GeneratePayoutModal from '@/components/payouts/GeneratePayoutModal.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import { usePayoutStore } from '@/store/modules/payouts'
import { useGroupStore } from '@/store/modules/groups'
import { useAuthStore } from '@/store/modules/auth'
import { useNotification } from '@/composables/useNotification'

const payoutStore = usePayoutStore()
const groupStore = useGroupStore()
const authStore = useAuthStore()
const { showSuccess, showError } = useNotification()

const showGenerateModal = ref(false)
const showMarkPaidDialog = ref(false)
const payoutToMark = ref(null)
const selectedPayout = ref(null)
const statusFilter = ref('')
const mentorFilter = ref(null)
const canManagePayouts = computed(() => authStore.userRole !== 'MENTOR')
const canCreatePayouts = computed(() => ['SUPERADMIN', 'BOSS'].includes(authStore.userRole))
const canMarkPayouts = computed(() => ['SUPERADMIN', 'BOSS'].includes(authStore.userRole))

const loadPayouts = async (params = {}) => {
  const mentorParam = canManagePayouts.value
    ? params.mentor ?? (mentorFilter.value || undefined)
    : undefined

  await payoutStore.fetchPayouts({
    page: params.page ?? payoutStore.pagination.currentPage,
    status: params.status ?? (statusFilter.value || undefined),
    mentor_id: mentorParam,
  })
  if (payoutStore.payouts.length) {
    const exists = selectedPayout.value
      ? payoutStore.payouts.some((p) => p.id === selectedPayout.value.id)
      : false
    if (!selectedPayout.value || !exists) {
      selectedPayout.value = payoutStore.payouts[0]
    }
  } else {
    selectedPayout.value = null
  }
}

onMounted(async () => {
  await loadPayouts({ page: 1 })
  if (canManagePayouts.value) {
    groupStore.fetchMentors()
  }
})

const handleStatusFilter = (status) => {
  statusFilter.value = status
  loadPayouts({ page: 1, status })
}

const handleMentorFilter = (mentorId) => {
  if (!canManagePayouts.value) return
  mentorFilter.value = mentorId
  loadPayouts({ page: 1, mentor: mentorId })
}

const handlePageChange = (page) => {
  loadPayouts({ page })
}

const handleGeneratePayout = async (payload) => {
  if (!canCreatePayouts.value) return
  const result = await payoutStore.generatePayout({
    mentor_id: payload.mentor_id,
    month: payload.month,
  })
  if (result.success) {
    showSuccess('Payout hisoblandi')
    showGenerateModal.value = false
    loadPayouts({ page: 1 })
  } else {
    showError(result.error?.detail || 'Payout yaratishda xatolik')
  }
}

const prepareMarkPaid = (payout) => {
  if (!canMarkPayouts.value) return
  payoutToMark.value = payout
  showMarkPaidDialog.value = true
}

const confirmMarkPaid = async () => {
  if (!canMarkPayouts.value || !payoutToMark.value) return
  const result = await payoutStore.markPaid(payoutToMark.value.id, { payment_details: {} })
  if (result.success) {
    showSuccess("Payout to'langan deb belgilandi")
    loadPayouts()
  } else {
    showError(result.error?.detail || 'Holatni yangilashda xatolik')
  }
  showMarkPaidDialog.value = false
}
</script>

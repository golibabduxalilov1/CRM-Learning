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
              To'lovlar
            </h1>
            <p class="text-sm text-slate-500 ml-3.5 mt-1">Oxirgi tushumlar va holatlar</p>
          </div>
          <button class="btn-primary p-2 rounded-md" @click="openCreateForm">Yangi to'lov</button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <PaymentCard
            label="Kutilayotgan to'lovlar"
            :value="paymentStore.totalPending"
            format="money"
            description="Tasdiqlanishi kerak bo'lgan to'lovlar"
            :icon="ClockIcon"
          />
          <PaymentCard
            label="To'langanlar"
            :value="paymentStore.totalPaid"
            format="money"
            description="Bu oyda qabul qilingan"
            :icon="BanknotesIcon"
          />
          <PaymentCard
            label="Umumiy yozuvlar"
            :value="paymentStore.pagination.count"
            description="Jami to'lovlar soni"
            :icon="DocumentTextIcon"
          />
        </div>

        <PaymentList
          :payments="paymentStore.payments"
          :loading="paymentStore.loading"
          :pagination="paymentStore.pagination"
          :search="searchQuery"
          :status="statusFilter"
          @create="openCreateForm"
          @search="handleSearch"
          @filter="handleFilter"
          @page-change="handlePageChange"
          @status="openStatusModal"
          @edit="openEditForm"
          @delete="prepareDelete"
        />
      </main>
    </div>
  </div>

  <Modal :show="showForm" :title="formTitle" size="lg" @close="closeForm">
    <PaymentForm
      :payment="selectedPayment"
      :students="studentStore.students"
      :groups="groupStore.groups"
      :loading="paymentStore.loading"
      @submit="handleFormSubmit"
      @cancel="closeForm"
    />
  </Modal>

  <PaymentStatusModal
    :show="showStatusModal"
    :payment="selectedPayment"
    :loading="paymentStore.loading"
    @close="closeStatusModal"
    @update="handleStatusUpdate"
  />

  <ConfirmDialog
    :show="showDeleteDialog"
    title="To'lovni o'chirish"
    message="Bu to'lov yozuvini o'chirmoqchimisiz?"
    confirm-text="Ha, o'chirish"
    cancel-text="Bekor qilish"
    @confirm="confirmDelete"
    @cancel="showDeleteDialog = false"
  />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Sidebar from '@/components/common/Sidebar.vue'
import Navbar from '@/components/common/Navbar.vue'
import PaymentList from '@/components/payments/PaymentList.vue'
import PaymentForm from '@/components/payments/PaymentForm.vue'
import PaymentCard from '@/components/payments/PaymentCard.vue'
import PaymentStatusModal from '@/components/payments/PaymentStatusModal.vue'
import Modal from '@/components/common/Modal.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import { usePaymentStore } from '@/store/modules/payments'
import { useGroupStore } from '@/store/modules/groups'
import { useStudentStore } from '@/store/modules/students'
import { useNotification } from '@/composables/useNotification'
import { BanknotesIcon, ClockIcon, DocumentTextIcon } from '@heroicons/vue/24/outline'

const paymentStore = usePaymentStore()
const groupStore = useGroupStore()
const studentStore = useStudentStore()
const { showSuccess, showError } = useNotification()

const showForm = ref(false)
const selectedPayment = ref(null)
const showStatusModal = ref(false)
const showDeleteDialog = ref(false)
const deletePaymentId = ref(null)
const searchQuery = ref('')
const statusFilter = ref('')

const formTitle = computed(() => (selectedPayment.value ? "To'lovni tahrirlash" : "Yangi to'lov"))

const loadPayments = (params = {}) => {
  paymentStore.fetchPayments({
    page: params.page ?? paymentStore.pagination.currentPage,
    search: params.search ?? (searchQuery.value || undefined),
    status: params.status ?? (statusFilter.value || undefined),
  })
}

onMounted(() => {
  loadPayments({ page: 1 })
  groupStore.fetchGroups({ page_size: 100 })
  studentStore.fetchStudents({ page_size: 100 })
})

const openCreateForm = () => {
  selectedPayment.value = null
  showForm.value = true
}

const openEditForm = (payment) => {
  selectedPayment.value = payment
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
  selectedPayment.value = null
}

const handleFormSubmit = async (payload) => {
  let result
  if (selectedPayment.value) {
    result = await paymentStore.updatePayment(selectedPayment.value.id, payload)
  } else {
    result = await paymentStore.createPayment(payload)
  }

  if (result.success) {
    showSuccess(selectedPayment.value ? "To'lov yangilandi" : "To'lov yaratildi")
    closeForm()
    loadPayments({ page: 1 })
  } else {
    showError(result.error?.detail || "Amalni bajarib bo'lmadi")
  }
}

const handleSearch = (query) => {
  searchQuery.value = query
  loadPayments({ page: 1, search: query })
}

const handleFilter = (status) => {
  statusFilter.value = status
  loadPayments({ page: 1, status })
}

const handlePageChange = (page) => {
  loadPayments({ page })
}

const openStatusModal = (payment) => {
  selectedPayment.value = payment
  showStatusModal.value = true
}

const closeStatusModal = () => {
  showStatusModal.value = false
}

const handleStatusUpdate = async (payload) => {
  if (!selectedPayment.value) return
  const result = await paymentStore.updatePaymentStatus(selectedPayment.value.id, payload)
  if (result.success) {
    showSuccess("To'lov holati yangilandi")
    closeStatusModal()
    loadPayments()
  } else {
    showError(result.error?.detail || 'Holatni yangilashda xatolik')
  }
}

const prepareDelete = (id) => {
  deletePaymentId.value = id
  showDeleteDialog.value = true
}

const confirmDelete = async () => {
  if (!deletePaymentId.value) return
  const result = await paymentStore.deletePayment(deletePaymentId.value)
  if (result.success) {
    showSuccess("To'lov o'chirildi")
    loadPayments()
  } else {
    showError(result.error?.detail || "To'lovni o'chirishda xatolik")
  }
  showDeleteDialog.value = false
}
</script>

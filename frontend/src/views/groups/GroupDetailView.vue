<template>
  <div class="flex min-h-screen bg-slate-50">
    <Sidebar />
    <div class="flex-1 flex flex-col min-w-0">
      <Navbar />
      <main class="flex-1 px-4 py-8 lg:px-8 space-y-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button
              class="p-2 rounded-md hover:bg-white hover:shadow-sm transition-all text-slate-500 hover:text-slate-700"
              @click="router.back()"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            <div>
              <h1 class="text-2xl font-bold text-slate-800">Guruh ma'lumotlari</h1>
              <p class="text-sm text-slate-500">Guruh va talabalar ro'yxati</p>
            </div>
          </div>
        </div>

        <Loading
          v-if="groupStore.detailLoading && !groupStore.currentGroup"
          text="Ma'lumot yuklanmoqda..."
        />

        <GroupDetail
          v-else
          :group="groupStore.currentGroup"
          :can-manage="!isMentor"
          @assign-mentor="openAssignModal"
          @edit-group="openEditForm"
          @delete-group="prepareDelete"
          @add-enrollment="openEnrollmentForm"
          @remove-enrollment="handleRemoveEnrollment"
          @update-enrollment="handleUpdateEnrollment"
        />
      </main>
    </div>
  </div>

  <Modal v-if="!isMentor" :show="showForm" :title="formTitle" size="lg" @close="closeForm">
    <GroupForm
      :group="groupStore.currentGroup"
      :mentors="groupStore.mentors"
      :loading="groupStore.loading"
      @submit="handleFormSubmit"
      @cancel="closeForm"
    />
  </Modal>

  <Modal
    v-if="!isMentor"
    :show="showAssignModal"
    title="Mentor tayinlash"
    @close="closeAssignModal"
  >
    <div class="space-y-4">
      <p class="text-sm text-gray-600">
        {{ groupStore.currentGroup?.name }} guruhiga mentor tanlang.
      </p>
      <select v-model="selectedMentorId" class="input-field">
        <option value="">Mentor tanlanmagan</option>
        <option v-for="mentor in groupStore.mentors" :key="mentor.id" :value="mentor.id">
          {{ mentor.first_name }} {{ mentor.last_name }}
        </option>
      </select>
      <div class="flex justify-end gap-3">
        <button class="btn-secondary p-2 rounded-md" @click="closeAssignModal">Bekor qilish</button>
        <button
          class="btn-primary p-2 rounded-md"
          :disabled="groupStore.loading"
          @click="handleAssignMentor"
        >
          {{ groupStore.loading ? 'Saqlanmoqda...' : 'Saqlash' }}
        </button>
      </div>
    </div>
  </Modal>

  <Modal
    v-if="!isMentor"
    :show="showEnrollmentModal"
    title="Talaba qo'shish"
    @close="closeEnrollmentModal"
  >
    <EnrollmentForm
      v-if="groupStore.currentGroup"
      :group-id="groupStore.currentGroup.id"
      :students="studentStore.students"
      :loading="groupStore.loading"
      @submit="handleEnrollmentSubmit"
      @cancel="closeEnrollmentModal"
    />
  </Modal>

  <ConfirmDialog
    v-if="!isMentor"
    :show="showDeleteDialog"
    title="Guruhni o'chirish"
    message="Bu guruhni o'chirmoqchimisiz? Barcha bog'langan ma'lumotlar o'chiriladi."
    confirm-text="Ha, o'chirish"
    cancel-text="Bekor qilish"
    @confirm="confirmDelete"
    @cancel="showDeleteDialog = false"
  />
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import Sidebar from '@/components/common/Sidebar.vue'
import Navbar from '@/components/common/Navbar.vue'
import Loading from '@/components/common/Loading.vue'
import Modal from '@/components/common/Modal.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import GroupDetail from '@/components/groups/GroupDetail.vue'
import GroupForm from '@/components/groups/GroupForm.vue'
import EnrollmentForm from '@/components/groups/EnrollmentForm.vue'
import { useGroupStore } from '@/store/modules/groups'
import { useStudentStore } from '@/store/modules/students'
import { useAuthStore } from '@/store/modules/auth'
import { useNotification } from '@/composables/useNotification'

const route = useRoute()
const router = useRouter()
const groupStore = useGroupStore()
const studentStore = useStudentStore()
const authStore = useAuthStore()
const { showSuccess, showError } = useNotification()

const showForm = ref(false)
const showAssignModal = ref(false)
const showEnrollmentModal = ref(false)
const showDeleteDialog = ref(false)
const selectedMentorId = ref('')

const formTitle = computed(() => `${groupStore.currentGroup?.name || ''} guruhini tahrirlash`)
const isMentor = computed(() => authStore.userRole === 'MENTOR')

const loadGroup = (id) => {
  if (id) {
    groupStore.fetchGroupById(id)
  }
}

onMounted(() => {
  loadGroup(route.params.id)
  if (!isMentor.value) {
    groupStore.fetchMentors()
    studentStore.fetchStudents({ page_size: 100 })
  }
})

watch(
  () => route.params.id,
  (id) => {
    loadGroup(id)
  },
)

const openEditForm = () => {
  if (isMentor.value) return
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
}

const handleFormSubmit = async (payload) => {
  if (isMentor.value || !groupStore.currentGroup) return
  const result = await groupStore.updateGroup(groupStore.currentGroup.id, payload)
  if (result.success) {
    showSuccess("Guruh ma'lumotlari yangilandi")
    closeForm()
  } else {
    showError(result.error?.detail || 'Guruhni yangilashda xatolik')
  }
}

const openAssignModal = () => {
  if (isMentor.value) return
  selectedMentorId.value =
    groupStore.currentGroup?.mentor || groupStore.currentGroup?.mentor_id || ''
  showAssignModal.value = true
}

const closeAssignModal = () => {
  showAssignModal.value = false
}

const handleAssignMentor = async () => {
  if (isMentor.value || !groupStore.currentGroup) return
  const result = await groupStore.assignMentor(groupStore.currentGroup.id, selectedMentorId.value)
  if (result.success) {
    showSuccess('Mentor tayinlandi')
    closeAssignModal()
  } else {
    showError(result.error?.detail || 'Mentor tayinlashda xatolik')
  }
}

const openEnrollmentForm = () => {
  if (isMentor.value) return
  showEnrollmentModal.value = true
}

const closeEnrollmentModal = () => {
  showEnrollmentModal.value = false
}

const handleEnrollmentSubmit = async (payload) => {
  if (isMentor.value) return
  const result = await groupStore.createEnrollment(payload)
  if (result.success) {
    showSuccess("Talaba guruhga qo'shildi")
    closeEnrollmentModal()
  } else {
    showError(result.error?.detail || "Talabani qo'shishda xatolik")
  }
}

const handleRemoveEnrollment = async (id) => {
  if (isMentor.value) return
  const result = await groupStore.deleteEnrollment(id)
  if (result.success) {
    showSuccess("Talaba guruhdan o'chirildi")
  } else {
    showError(result.error?.detail || "Talabani o'chirishda xatolik")
  }
}

const handleUpdateEnrollment = async ({ id, status }) => {
  if (isMentor.value) return
  const result = await groupStore.updateEnrollment(id, { status })
  if (result.success) {
    showSuccess('Talaba holati yangilandi')
  } else {
    showError(result.error?.detail || 'Holatni yangilashda xatolik')
  }
}

const prepareDelete = () => {
  if (isMentor.value) return
  showDeleteDialog.value = true
}

const confirmDelete = async () => {
  if (isMentor.value || !groupStore.currentGroup) return
  const result = await groupStore.deleteGroup(groupStore.currentGroup.id)
  if (result.success) {
    showSuccess("Guruh o'chirildi")
    router.push('/groups')
  } else {
    showError(result.error?.detail || "Guruhni o'chirishda xatolik")
  }
  showDeleteDialog.value = false
}
</script>

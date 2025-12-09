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
              Guruhlar
            </h1>
            <p class="text-sm text-slate-500 ml-3.5 mt-1">
              Faol va rejalashtirilgan guruhlar ro'yxati
            </p>
          </div>
          <button
            v-if="!isMentor"
            class="btn-primary flex items-center gap-2 p-2 rounded-md"
            @click="openCreateForm"
          >
            <PlusIcon class="w-5 h-5" />
            Yangi guruh
          </button>
        </div>

        <GroupList
          :groups="groupStore.groups"
          :mentors="groupStore.mentors"
          :loading="groupStore.loading"
          :pagination="groupStore.pagination"
          :search="groupStore.filters.search"
          :mentor-filter="groupStore.filters.mentor"
          :can-manage="!isMentor"
          @search="handleSearch"
          @filter="handleMentorFilter"
          @page-change="handlePageChange"
          @view="handleView"
          @edit="handleEdit"
          @assign-mentor="openAssignMentor"
          @delete="prepareDelete"
        />
      </main>
    </div>
  </div>

  <Modal
    v-if="!isMentor"
    :show="showForm"
    :title="formTitle"
    size="lg"
    @close="closeForm"
  >
    <GroupForm
      :group="selectedGroup"
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
        {{ assignGroup?.name }} guruhiga mentor tanlang.
      </p>
      <select
        v-model="selectedMentorId"
        class="input-field"
      >
        <option value="">
          Mentor tanlanmagan
        </option>
        <option
          v-for="mentor in groupStore.mentors"
          :key="mentor.id"
          :value="mentor.id"
        >
          {{ mentor.first_name }} {{ mentor.last_name }}
        </option>
      </select>
      <div class="flex justify-end gap-3">
        <button
          class="btn-secondary p-2 rounded-md"
          @click="closeAssignModal"
        >
          Bekor qilish
        </button>
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

  <ConfirmDialog
    v-if="!isMentor"
    :show="showDeleteDialog"
    title="Guruhni o'chirish"
    message="Bu guruhni o'chirmoqchimisiz? Unga bog'langan ma'lumotlar ham o'chiriladi."
    confirm-text="Ha, o'chirish"
    cancel-text="Bekor qilish"
    @confirm="confirmDelete"
    @cancel="showDeleteDialog = false"
  />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { PlusIcon } from '@heroicons/vue/24/outline'
import Sidebar from '@/components/common/Sidebar.vue'
import Navbar from '@/components/common/Navbar.vue'
import GroupList from '@/components/groups/GroupList.vue'
import GroupForm from '@/components/groups/GroupForm.vue'
import Modal from '@/components/common/Modal.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import { useGroupStore } from '@/store/modules/groups'
import { useNotification } from '@/composables/useNotification'
import { useAuthStore } from '@/store/modules/auth'

const router = useRouter()
const groupStore = useGroupStore()
const authStore = useAuthStore()
const { showSuccess, showError } = useNotification()

const showForm = ref(false)
const selectedGroup = ref(null)
const showAssignModal = ref(false)
const assignGroup = ref(null)
const selectedMentorId = ref('')
const showDeleteDialog = ref(false)
const deleteGroupId = ref(null)

const formTitle = computed(() => (selectedGroup.value ? 'Guruhni tahrirlash' : "Yangi guruh yaratish"))
const isMentor = computed(() => authStore.userRole === 'MENTOR')

onMounted(() => {
  groupStore.fetchGroups()
  if (!isMentor.value) {
    groupStore.fetchMentors()
  }
})

const openCreateForm = () => {
  if (isMentor.value) return
  selectedGroup.value = null
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
  selectedGroup.value = null
}

const handleEdit = (group) => {
  if (isMentor.value) return
  selectedGroup.value = group
  showForm.value = true
}

const handleFormSubmit = async (payload) => {
  const action = selectedGroup.value
    ? groupStore.updateGroup(selectedGroup.value.id, payload)
    : groupStore.createGroup(payload)

  const result = await action
  if (result.success) {
    showSuccess(selectedGroup.value ? 'Guruh yangilandi' : 'Guruh yaratildi')
    closeForm()
    groupStore.fetchGroups()
  } else {
    showError(result.error?.detail || 'Amalni bajarib bo\'lmadi')
  }
}

const handleSearch = (query) => {
  groupStore.fetchGroups({ search: query, page: 1 })
}

const handleMentorFilter = (mentorId) => {
  groupStore.fetchGroups({ mentor: mentorId || null, page: 1 })
}

const handlePageChange = (page) => {
  groupStore.fetchGroups({ page })
}

const handleView = (id) => {
  router.push(`/groups/${id}`)
}

const openAssignMentor = (group) => {
  if (isMentor.value) return
  assignGroup.value = group
  selectedMentorId.value = group.mentor || group.mentor_id || ''
  showAssignModal.value = true
}

const closeAssignModal = () => {
  showAssignModal.value = false
  assignGroup.value = null
  selectedMentorId.value = ''
}

const handleAssignMentor = async () => {
  if (!assignGroup.value) return
  const result = await groupStore.assignMentor(assignGroup.value.id, selectedMentorId.value)
  if (result.success) {
    showSuccess('Mentor tayinlandi')
    closeAssignModal()
  } else {
    showError(result.error?.detail || 'Mentor tayinlashda xatolik')
  }
}

const prepareDelete = (group) => {
  if (isMentor.value) return
  deleteGroupId.value = group.id
  showDeleteDialog.value = true
}

const confirmDelete = async () => {
  if (!deleteGroupId.value) return
  const result = await groupStore.deleteGroup(deleteGroupId.value)
  if (result.success) {
    showSuccess('Guruh o\'chirildi')
    groupStore.fetchGroups()
  } else {
    showError(result.error?.detail || 'Guruhni o\'chirishda xatolik')
  }
  showDeleteDialog.value = false
}
</script>

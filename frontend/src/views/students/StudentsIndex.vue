<template>
  <div class="flex min-h-screen bg-slate-50">
    <Sidebar />
    <div class="flex-1 flex flex-col min-w-0">
      <Navbar />
      <main class="flex-1 px-4 py-8 lg:px-8">
        <StudentList
          v-if="!showForm"
          :can-manage="canManageStudents"
          @create="handleCreate"
          @view="handleView"
          @edit="handleEdit"
          @delete="handleDelete"
          @page-change="handlePageChange"
          @search="handleSearch"
        />

        <StudentForm
          v-else-if="canManageStudents"
          :student="selectedStudent"
          @success="handleFormSuccess"
          @cancel="handleFormCancel"
        />

        <ConfirmDialog
          v-if="canManageStudents"
          :show="showDeleteDialog"
          title="Talabani o'chirish"
          message="Rostdan ham bu talabani o'chirmoqchimisiz? Bu amalni bekor qilib bo'lmaydi."
          confirm-text="Ha, o'chirish"
          cancel-text="Yo'q"
          @confirm="confirmDelete"
          @cancel="showDeleteDialog = false"
        />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStudentStore } from '@/store/modules/students'
import { useNotification } from '@/composables/useNotification'
import { useAuthStore } from '@/store/modules/auth'
import Navbar from '@/components/common/Navbar.vue'
import Sidebar from '@/components/common/Sidebar.vue'
import StudentList from '@/components/students/StudentList.vue'
import StudentForm from '@/components/students/StudentForm.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'

const router = useRouter()
const studentStore = useStudentStore()
const authStore = useAuthStore()
const { showSuccess, showError } = useNotification()

const showForm = ref(false)
const selectedStudent = ref(null)
const showDeleteDialog = ref(false)
const deleteStudentId = ref(null)
const currentPage = ref(1)
const searchQuery = ref('')

const canManageStudents = computed(() => authStore.userRole !== 'MENTOR')

onMounted(() => {
  loadStudents()
})

const loadStudents = () => {
  studentStore.fetchStudents({
    page: currentPage.value,
    search: searchQuery.value,
  })
}

const handleCreate = () => {
  if (!canManageStudents.value) return
  selectedStudent.value = null
  showForm.value = true
}

const handleView = (id) => {
  router.push(`/students/${id}`)
}

const handleEdit = (student) => {
  if (!canManageStudents.value) return
  selectedStudent.value = student
  showForm.value = true
}

const handleDelete = (id) => {
  if (!canManageStudents.value) return
  deleteStudentId.value = id
  showDeleteDialog.value = true
}

const confirmDelete = async () => {
  const result = await studentStore.deleteStudent(deleteStudentId.value)
  if (result.success) {
    showSuccess("Talaba muvaffaqiyatli o'chirildi")
    loadStudents()
  } else {
    showError("Talabani o'chirishda xatolik")
  }
  showDeleteDialog.value = false
  deleteStudentId.value = null
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadStudents()
}

const handleSearch = (query) => {
  searchQuery.value = query
  currentPage.value = 1
  loadStudents()
}

const handleFormSuccess = (payload) => {
  const mode = payload?.mode === 'update' ? 'update' : 'create'
  showForm.value = false
  selectedStudent.value = null
  showSuccess(mode === 'update' ? 'Talaba yangilandi' : 'Talaba yaratildi')
  loadStudents()
}

const handleFormCancel = () => {
  showForm.value = false
  selectedStudent.value = null
}
</script>

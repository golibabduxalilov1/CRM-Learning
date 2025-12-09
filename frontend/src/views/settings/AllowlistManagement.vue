<template>
  <div class="flex bg-gray-50 min-h-screen">
    <Sidebar />
    <div class="flex-1">
      <Navbar />
      <div class="p-6 space-y-6">
        <h1 class="text-3xl font-bold text-gray-900">Email allowlist</h1>
        <p class="text-gray-500">
          Faqat shu ro'yxatdagi email manzillar ro'yxatdan o'tishi mumkin.
        </p>

        <div class="card space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <input
              v-model="newEmail"
              type="email"
              class="input-field md:col-span-2"
              placeholder="team@company.uz"
            />
            <select v-model="selectedRole" class="input-field">
              <option v-for="role in roleOptions" :key="role.value" :value="role.value">
                {{ role.label }}
              </option>
            </select>
          </div>
          <div class="flex justify-end">
            <button
              class="btn-primary p-2 rounded-md"
              :disabled="allowlistStore.loading"
              @click="handleAddEmail"
            >
              {{ allowlistStore.loading ? "Qo'shilmoqda..." : "Allowlistga qo'shish" }}
            </button>
          </div>
        </div>

        <AllowlistTable :entries="allowlistStore.entries" @remove="handleRemove" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '@/components/common/Sidebar.vue'
import Navbar from '@/components/common/Navbar.vue'
import AllowlistTable from '@/components/settings/AllowlistTable.vue'
import { useAllowlistStore } from '@/store/modules/allowlist'
import { useNotification } from '@/composables/useNotification'

const allowlistStore = useAllowlistStore()
const { showSuccess, showError } = useNotification()

const newEmail = ref('')
const selectedRole = ref('ADMIN')

const roleOptions = [
  { value: 'SUPERADMIN', label: 'Superadmin' },
  { value: 'BOSS', label: 'Boss' },
  { value: 'ADMIN', label: 'Admin' },
  { value: 'MENTOR', label: 'Mentor' },
]

onMounted(() => {
  allowlistStore.fetchEntries()
})

const handleAddEmail = async () => {
  if (!newEmail.value) {
    showError('Email manzilini kiriting')
    return
  }
  const result = await allowlistStore.addEntry({
    email: newEmail.value,
    role: selectedRole.value,
  })
  if (result.success) {
    showSuccess("Email allowlistga qo'shildi")
    newEmail.value = ''
  } else {
    showError(result.error?.detail || "Allowlistga qo'shishda xatolik")
  }
}

const handleRemove = async (id) => {
  const result = await allowlistStore.removeEntry(id)
  if (result.success) {
    showSuccess("Email o'chirildi")
  } else {
    showError(result.error?.detail || "Emailni o'chirishda xatolik")
  }
}
</script>

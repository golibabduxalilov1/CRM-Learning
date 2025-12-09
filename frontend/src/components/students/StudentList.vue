<template>
  <div class="space-y-5">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div class="flex flex-1 gap-3">
        <input
          v-model="searchValue"
          type="text"
          class="input-field"
          placeholder="Ism, telefon yoki email bo'yicha qidiring"
          @keyup.enter="handleSearch"
        />
        <button class="btn-secondary p-2 rounded-md" @click="handleSearch">Qidirish</button>
      </div>
      <button
        v-if="canManage"
        class="btn-primary flex items-center justify-center gap-2 p-2 rounded-md"
        @click="emit('create')"
      >
        <PlusIcon class="w-5 h-5" />
        Yangi talaba
      </button>
    </div>

    <div v-if="students.length" class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>Talaba</th>
            <th>Telefon</th>
            <th>Email</th>
            <th>Holati</th>
            <th>Qo'shilgan sana</th>
            <th class="text-right">
              {{ canManage ? 'Amallar' : "Ko'rish" }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in students" :key="student.id">
            <td class="font-semibold">{{ student.first_name }} {{ student.last_name }}</td>
            <td>{{ student.phone || '-' }}</td>
            <td>{{ student.email || '-' }}</td>
            <td>
              <span :class="[student.is_active ? 'badge-success' : 'badge-danger']" class="badge">
                {{ student.is_active ? 'Faol' : 'Nofaol' }}
              </span>
            </td>
            <td>{{ formatDate(student.created_at) }}</td>
            <td class="text-right space-x-2">
              <button class="btn-secondary px-3 py-1 p-2 rounded-md" @click="emit('view', student.id)">
                Ko'rish
              </button>
              <template v-if="canManage">
                <button class="btn-secondary px-3 py-1 p-2 rounded-md" @click="emit('edit', student)">
                  Tahrirlash
                </button>
                <button class="btn-danger px-3 py-1 p-2 rounded-md" @click="emit('delete', student.id)">
                  O'chirish
                </button>
              </template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else-if="!studentStore.loading" class="card text-center text-gray-500 p-12">
      Hozircha hech qanday talaba topilmadi.
    </div>

    <Loading v-if="studentStore.loading" text="Talabalar yuklanmoqda..." />

    <Pagination
      v-if="students.length"
      :current-page="studentStore.pagination.currentPage"
      :total-pages="studentStore.pagination.totalPages"
      :total-count="studentStore.pagination.count"
      @page-change="emit('page-change', $event)"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { PlusIcon } from '@heroicons/vue/24/outline'
import { useStudentStore } from '@/store/modules/students'
import { formatDate } from '@/utils/helpers'
import Loading from '@/components/common/Loading.vue'
import Pagination from '@/components/common/Pagination.vue'

const emit = defineEmits(['create', 'view', 'edit', 'delete', 'page-change', 'search'])
const props = defineProps({
  canManage: {
    type: Boolean,
    default: true,
  },
})
const studentStore = useStudentStore()

const searchValue = ref('')

const students = computed(() => studentStore.students || [])

const handleSearch = () => {
  emit('search', searchValue.value.trim())
}
</script>

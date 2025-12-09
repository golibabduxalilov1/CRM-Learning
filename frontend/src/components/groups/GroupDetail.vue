<template>
  <div v-if="group" class="grid grid-cols-1 lg:grid-cols-1 gap-6">
    <div class="lg:col-span-2 space-y-6">
      <div class="glass-panel p-6 relative overflow-hidden rounded-md">
        <div class="absolute top-0 right-0 p-4 opacity-10">
          <AcademicCapIcon class="w-32 h-32 text-primary-500" />
        </div>

        <div class="relative z-10">
          <div class="flex items-start justify-between mb-6">
            <div>
              <span
                class="px-3 py-1 rounded-full text-xs font-medium bg-primary-50 text-primary-700 border border-primary-100 mb-2 inline-block"
              >
                {{ group.subject }}
              </span>
              <h1 class="text-3xl font-bold text-slate-800 mb-1">{{ group.name }}</h1>
              <div class="flex items-center gap-2 text-slate-500">
                <UserIcon class="w-4 h-4" />
                <span>Mentor:</span>
                <span class="font-medium text-slate-700">{{
                  group.mentor_name || 'Tayinlanmagan'
                }}</span>
              </div>
            </div>
            <div v-if="canManage" class="flex gap-2">
              <button
                class="btn-secondary p-2 rounded-md"
                @click="$emit('edit-group')"
                title="Tahrirlash"
              >
                <PencilIcon class="w-5 h-5" />
              </button>
              <button
                class="btn-danger p-2 rounded-md"
                @click="$emit('delete-group')"
                title="O'chirish"
              >
                <TrashIcon class="w-5 h-5" />
              </button>
            </div>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-6 border-t border-white/20">
            <div>
              <p class="text-xs text-slate-500 mb-1">Boshlanish</p>
              <p class="font-medium text-slate-800">{{ formatDate(group.start_date) }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500 mb-1">Tugash</p>
              <p class="font-medium text-slate-800">
                {{ group.end_date ? formatDate(group.end_date) : '-' }}
              </p>
            </div>
            <div>
              <p class="text-xs text-slate-500 mb-1">Talabalar</p>
              <p class="font-medium text-slate-800">
                {{ group.students_count }} / {{ group.max_students }}
              </p>
            </div>
            <div>
              <p class="text-xs text-slate-500 mb-1">Narx</p>
              <p class="font-medium text-primary-600">{{ formatMoney(group.price_per_month) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Students List -->
      <div class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
        <div class="p-6 border-b border-slate-50 flex items-center justify-between">
          <h2 class="text-lg font-bold text-slate-800 flex items-center gap-2">
            <UsersIcon class="w-5 h-5 text-primary-500" />
            Talabalar ro'yxati
          </h2>
          <button
            v-if="canManage"
            class="btn-primary text-sm py-2 p-2 rounded-md"
            @click="$emit('add-enrollment')"
          >
            <PlusIcon class="w-4 h-4 mr-1" />
            Talaba qo'shish
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-slate-50 text-xs uppercase text-slate-400 font-medium">
              <tr>
                <th class="px-6 py-3 text-left tracking-wider">Talaba</th>
                <th class="px-6 py-3 text-left tracking-wider">Holat</th>
                <th class="px-6 py-3 text-left tracking-wider">Qo'shilgan sana</th>
                <th class="px-6 py-3 text-right tracking-wider">Amallar</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr
                v-for="enrollment in group.enrollments"
                :key="enrollment.id"
                class="hover:bg-slate-50/50 transition-colors"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div
                      class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-100 to-violet-100 flex items-center justify-center text-primary-600 font-bold text-xs mr-3"
                    >
                      {{ (enrollment.student_name || formatStudentName(enrollment))?.[0] }}
                    </div>
                    <span class="font-medium text-slate-700">{{
                      enrollment.student_name || formatStudentName(enrollment)
                    }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <select
                    v-model="localStatuses[enrollment.id]"
                    class="text-xs font-medium rounded-full px-2 py-1 border-0 bg-slate-100 text-slate-600 focus:ring-2 focus:ring-primary-500 cursor-pointer"
                    :class="{
                      'bg-emerald-50 text-emerald-700': localStatuses[enrollment.id] === 'ACTIVE',
                      'bg-amber-50 text-amber-700': localStatuses[enrollment.id] === 'PAUSED',
                      'bg-blue-50 text-blue-700': localStatuses[enrollment.id] === 'COMPLETED',
                      'bg-rose-50 text-rose-700': localStatuses[enrollment.id] === 'DROPPED',
                    }"
                    @change="handleStatusChange(enrollment.id, localStatuses[enrollment.id])"
                    :disabled="!canManage"
                  >
                    <option
                      v-for="status in enrollmentStatuses"
                      :key="status.value"
                      :value="status.value"
                    >
                      {{ status.label }}
                    </option>
                  </select>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                  {{ formatDate(enrollment.enrolled_date) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right">
                  <button
                    v-if="canManage"
                    class="text-slate-400 hover:text-rose-500 transition-colors p-2 rounded-md"
                    @click="$emit('remove-enrollment', enrollment.id)"
                    title="Guruhdan chiqarish"
                  >
                    <TrashIcon class="w-4 h-4" />
                  </button>
                </td>
              </tr>
              <tr v-if="!group.enrollments?.length">
                <td colspan="4" class="px-6 py-8 text-center text-slate-400 text-sm">
                  Guruhda talabalar mavjud emas
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Sidebar Actions -->
    <div v-if="canManage" class="space-y-6">
      <div class="bg-white rounded-2xl border border-slate-100 p-6 shadow-sm">
        <h3 class="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4">Boshqaruv</h3>
        <div class="space-y-3">
          <button
            class="w-full btn-secondary justify-start p-2 rounded-md"
            @click="$emit('assign-mentor')"
          >
            <UserIcon class="w-4 h-4 mr-2" />
            Mentor tayinlash
          </button>
          <button
            class="w-full btn-secondary justify-start p-2 rounded-md"
            @click="$emit('edit-group')"
          >
            <PencilIcon class="w-4 h-4 mr-2" />
            Guruhni tahrirlash
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="text-center py-12">
    <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-100 mb-4">
      <AcademicCapIcon class="w-8 h-8 text-slate-400" />
    </div>
    <h3 class="text-lg font-medium text-slate-900">Guruh topilmadi</h3>
  </div>
</template>

<script setup>
import { reactive, watch, computed } from 'vue'
import {
  AcademicCapIcon,
  UserIcon,
  PencilIcon,
  TrashIcon,
  UsersIcon,
  PlusIcon,
} from '@heroicons/vue/24/outline'
import { ENROLLMENT_STATUS } from '@/utils/constants'
import { formatDate, formatMoney } from '@/utils/helpers'

const props = defineProps({
  group: {
    type: Object,
    default: null,
  },
  canManage: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits([
  'assign-mentor',
  'edit-group',
  'delete-group',
  'add-enrollment',
  'update-enrollment',
  'remove-enrollment',
])

const localStatuses = reactive({})

watch(
  () => props.group?.enrollments,
  (enrollments) => {
    Object.keys(localStatuses).forEach((key) => delete localStatuses[key])
    enrollments?.forEach((enrollment) => {
      localStatuses[enrollment.id] = enrollment.status
    })
  },
  { immediate: true },
)

const enrollmentStatuses = computed(() =>
  Object.entries(ENROLLMENT_STATUS).map(([value]) => ({
    value,
    label: formatStatusLabel(value),
  })),
)

const formatStatusLabel = (value) => {
  const labels = {
    ACTIVE: 'Faol',
    PAUSED: "To'xtatilgan",
    COMPLETED: 'Tugatilgan',
    DROPPED: 'Tashlab ketgan',
  }
  return labels[value] || value
}

const handleStatusChange = (id, status) => {
  emit('update-enrollment', { id, status })
}

const formatStudentName = (enrollment) => {
  if (!enrollment?.student) return '-'
  return `${enrollment.student.first_name} ${enrollment.student.last_name}`
}
</script>

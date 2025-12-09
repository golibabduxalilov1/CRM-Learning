<template>
  <div class="card max-w-3xl mx-auto p-4">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">
          {{ isEdit ? 'Talabani tahrirlash' : "Yangi talaba qo'shish" }}
        </h2>
        <p class="text-gray-500 text-sm">
          Asosiy ma'lumotlarni kiriting va saqlash tugmasini bosing
        </p>
      </div>
    </div>

    <form class="space-y-5" @submit.prevent="handleSubmit">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Ism</label>
          <input v-model="form.first_name" type="text" required class="input-field" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Familiya</label>
          <input v-model="form.last_name" type="text" required class="input-field" />
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Telefon</label>
          <input
            v-model="form.phone"
            type="tel"
            class="input-field"
            placeholder="+998 90 123 45 67"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="form.email"
            type="email"
            class="input-field"
            placeholder="student@example.com"
          />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Qo'shimcha eslatma</label>
        <textarea v-model="form.notes" rows="10" class="input-field" placeholder="Ixtiyoriy" />
      </div>

      <div class="flex items-center space-x-2">
        <input
          id="is_active"
          v-model="form.is_active"
          type="checkbox"
          class="h-4 w-4 text-primary-600"
        />
        <label for="is_active" class="text-sm text-gray-700">Talaba faol</label>
      </div>

      <div
        v-if="error"
        class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm"
      >
        {{ error }}
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <button type="submit" class="btn-primary p-2 rounded-md" :disabled="studentStore.loading">
          {{ studentStore.loading ? 'Saqlanmoqda...' : isEdit ? 'Yangilash' : "Qo'shish" }}
        </button>
        <button class="btn-secondary p-2 rounded-md" @click="emit('cancel')">Bekor qilish</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useStudentStore } from '@/store/modules/students'

const props = defineProps({
  student: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['success', 'cancel'])
const studentStore = useStudentStore()
const form = ref(getInitialForm())
const error = ref('')

const isEdit = computed(() => Boolean(props.student?.id))

watch(
  () => props.student,
  (value) => {
    form.value = value
      ? {
          first_name: value.first_name || '',
          last_name: value.last_name || '',
          phone: value.phone || '',
          email: value.email || '',
          notes: value.notes || '',
          is_active: value.is_active ?? true,
        }
      : getInitialForm()
  },
  { immediate: true },
)

async function handleSubmit() {
  error.value = ''
  const payload = { ...form.value }
  let result

  if (isEdit.value) {
    result = await studentStore.updateStudent(props.student.id, payload)
  } else {
    result = await studentStore.createStudent(payload)
  }

  if (result.success) {
    emit('success', { mode: isEdit.value ? 'update' : 'create' })
  } else {
    const detail = result.error?.detail || 'Saqlashda xatolik yuz berdi'
    error.value = detail
  }
}

function getInitialForm() {
  return {
    first_name: '',
    last_name: '',
    phone: '',
    email: '',
    notes: '',
    is_active: true,
  }
}
</script>

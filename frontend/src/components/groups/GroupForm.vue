<template>
  <form
    class="space-y-4"
    @submit.prevent="handleSubmit"
  >
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Guruh nomi</label>
        <input
          v-model="form.name"
          type="text"
          class="input-field"
          required
          placeholder="Frontend Pro 6"
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Yo'nalish</label>
        <input
          v-model="form.subject"
          type="text"
          class="input-field"
          required
          placeholder="Frontend"
        >
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Mentor</label>
        <select
          v-model="form.mentor"
          class="input-field"
        >
          <option value="">
            Tayinlanmagan
          </option>
          <option
            v-for="mentor in mentors"
            :key="mentor.id"
            :value="mentor.id"
          >
            {{ mentor.first_name }} {{ mentor.last_name }}
          </option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Talabalar limiti</label>
        <input
          v-model.number="form.max_students"
          type="number"
          min="1"
          class="input-field"
          required
        >
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Boshlanish sanasi</label>
        <input
          v-model="form.start_date"
          type="date"
          class="input-field"
          required
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Tugash sanasi</label>
        <input
          v-model="form.end_date"
          type="date"
          class="input-field"
        >
      </div>
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Oylik narx (so'm)</label>
      <input
        v-model.number="form.price_per_month"
        type="number"
        min="0"
        step="50000"
        class="input-field"
        required
      >
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Qo'shimcha ma'lumot</label>
      <textarea
        v-model="form.description"
        rows="3"
        class="input-field"
        placeholder="Dars jadvali, joylashuv va boshqalar"
      />
    </div>

    <div class="flex items-center justify-end gap-3 pt-2">
      <button
        type="button"
        class="btn-secondary p-2 rounded-md"
        :disabled="loading"
        @click="emit('cancel')"
      >
        Bekor qilish
      </button>
      <button
        type="submit"
        class="btn-primary p-2 rounded-md"
        :disabled="loading"
      >
        {{ loading ? 'Saqlanmoqda...' : isEdit ? 'Yangilash' : "Guruh yaratish" }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { computed, reactive, watch } from 'vue'

const props = defineProps({
  group: {
    type: Object,
    default: null,
  },
  mentors: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive(getInitialForm(props.group))

watch(
  () => props.group,
  (value) => {
    Object.assign(form, getInitialForm(value))
  },
  { immediate: true }
)

const isEdit = computed(() => Boolean(props.group?.id))

function getInitialForm(group) {
  return {
    name: group?.name || '',
    subject: group?.subject || '',
    mentor: group?.mentor || group?.mentor_id || '',
    max_students: group?.max_students || 20,
    start_date: group?.start_date || '',
    end_date: group?.end_date || '',
    price_per_month: group?.price_per_month || 0,
    description: group?.description || '',
  }
}

const handleSubmit = () => {
  emit('submit', {
    ...form,
    mentor: form.mentor || null,
    max_students: Number(form.max_students),
    price_per_month: Number(form.price_per_month),
  })
}
</script>

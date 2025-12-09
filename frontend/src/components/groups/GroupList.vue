<template>
  <div class="space-y-5">
    <div :class="['grid grid-cols-1 gap-4', canManage ? 'lg:grid-cols-3' : 'lg:grid-cols-1 md:grid-cols-2']">
      <input
        v-model="localSearch"
        type="text"
        class="input-field"
        placeholder="Guruh nomi yoki yo'nalish bo'yicha qidiring"
        @keyup.enter="handleSearch"
      >
      <select
        v-if="canManage"
        v-model="selectedMentor"
        class="input-field"
        @change="handleFilter"
      >
        <option value="">
          Barcha mentorlar
        </option>
        <option
          v-for="mentor in mentors"
          :key="mentor.id"
          :value="mentor.id"
        >
          {{ mentor.first_name }} {{ mentor.last_name }}
        </option>
      </select>
      <button
        v-if="canManage"
        class="btn-secondary p-2 rounded-md"
        @click="handleReset"
      >
        Filtrlarni tozalash
      </button>
    </div>

    <Loading
      v-if="loading"
      text="Guruhlar yuklanmoqda..."
    />

    <div v-else>
      <div
        v-if="groups.length"
        class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4"
      >
        <GroupCard
          v-for="group in groups"
          :key="group.id"
          :group="group"
          :can-manage="canManage"
          @click="$emit('view', group.id)"
          @edit="$emit('edit', group)"
          @assign-mentor="$emit('assign-mentor', group)"
          @delete="$emit('delete', group)"
        />
      </div>
      <div
        v-else
        class="card text-center text-gray-500"
      >
        Hozircha hech qanday guruh topilmadi.
      </div>
    </div>

    <Pagination
      v-if="groups.length && pagination.totalPages > 1"
      :current-page="pagination.currentPage"
      :total-pages="pagination.totalPages"
      :total-count="pagination.count"
      @page-change="$emit('page-change', $event)"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import GroupCard from './GroupCard.vue'
import Loading from '@/components/common/Loading.vue'
import Pagination from '@/components/common/Pagination.vue'

const props = defineProps({
  groups: {
    type: Array,
    default: () => [],
  },
  mentors: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  pagination: {
    type: Object,
    default: () => ({ count: 0, totalPages: 1, currentPage: 1 }),
  },
  search: {
    type: String,
    default: '',
  },
  mentorFilter: {
    type: [String, Number, null],
    default: '',
  },
  canManage: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['search', 'page-change', 'view', 'edit', 'assign-mentor', 'filter', 'delete'])

const localSearch = ref(props.search || '')
const selectedMentor = ref(props.mentorFilter || '')

watch(
  () => props.search,
  (value) => {
    localSearch.value = value || ''
  }
)

watch(
  () => props.mentorFilter,
  (value) => {
    selectedMentor.value = value || ''
  }
)

const handleSearch = () => {
  emit('search', localSearch.value.trim())
}

const handleFilter = () => {
  emit('filter', selectedMentor.value || null)
}

const handleReset = () => {
  localSearch.value = ''
  selectedMentor.value = ''
  emit('search', '')
  emit('filter', null)
}
</script>

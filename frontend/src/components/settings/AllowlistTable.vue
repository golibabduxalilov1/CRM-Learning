<template>
  <div class="card overflow-x-auto">
    <table class="table">
      <thead>
        <tr>
          <th>Email</th>
          <th>Rol</th>
          <th>Qo'shilgan</th>
          <th class="text-right">
            Amallar
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="entry in entries"
          :key="entry.id"
        >
          <td class="font-medium">
            {{ entry.email }}
          </td>
          <td>{{ formatRole(entry.role) }}</td>
          <td>{{ formatDate(entry.created_at) }}</td>
          <td class="text-right">
            <button
              class="text-danger-600 hover:underline text-sm p-2 rounded-md"
              @click="$emit('remove', entry.id)"
            >
              O'chirish
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <div
      v-if="!entries.length"
      class="text-center text-gray-500 py-6"
    >
      Allowlist bo'sh.
    </div>
  </div>
</template>

<script setup>
import { formatDate } from '@/utils/helpers'

defineProps({
  entries: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['remove'])

const formatRole = (role) => {
  const map = {
    SUPERADMIN: 'Superadmin',
    BOSS: 'Boss',
    ADMIN: 'Admin',
    MENTOR: 'Mentor',
  }
  return map[role] || role
}
</script>

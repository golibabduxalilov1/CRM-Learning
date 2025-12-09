<template>
  <Modal
    :show="show"
    :title="title"
    @close="handleCancel"
  >
    <div class="mt-2">
      <p class="text-sm text-gray-500">
        {{ message }}
      </p>
    </div>

    <template #footer>
      <button
        class="btn-danger mr-3 p-2 rounded-md"
        @click="handleConfirm"
      >
        {{ confirmText }}
      </button>
      <button
        class="btn-secondary p-2 rounded-md"
        @click="handleCancel"
      >
        {{ cancelText }}
      </button>
    </template>
  </Modal>
</template>

<script setup>
import Modal from "./Modal.vue";

defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: "Tasdiqlash",
  },
  message: {
    type: String,
    required: true,
  },
  confirmText: {
    type: String,
    default: "Tasdiqlash",
  },
  cancelText: {
    type: String,
    default: "Bekor qilish",
  },
});

const emit = defineEmits(["confirm", "cancel"]);

const handleConfirm = () => {
  emit("confirm");
};

const handleCancel = () => {
  emit("cancel");
};
</script>

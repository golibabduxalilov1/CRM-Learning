<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="text-center">
      <div class="mb-8">
        <div
          class="inline-flex items-center justify-center w-32 h-32 bg-primary-100 rounded-full mb-4"
        >
          <ExclamationTriangleIcon class="w-20 h-20 text-primary-600" />
        </div>
      </div>

      <h1 class="text-9xl font-extrabold text-primary-600 mb-4">
        404
      </h1>
      <h2 class="text-4xl font-bold text-gray-900 mb-4">
        Sahifa topilmadi
      </h2>
      <p class="text-xl text-gray-600 mb-8 max-w-md mx-auto">
        Siz qidirayotgan sahifa mavjud emas yoki ko'chirilgan bo'lishi mumkin.
      </p>

      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <router-link
          to="/"
          class="btn-primary"
        >
          <HomeIcon class="w-5 h-5 inline mr-2" />
          Bosh sahifa
        </router-link>
        <button
          class="btn-secondary p-2 rounded-md"
          @click="$router.go(-1)"
        >
          <ArrowLeftIcon class="w-5 h-5 inline mr-2" />
          Ortga qaytish
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ExclamationTriangleIcon, HomeIcon, ArrowLeftIcon } from '@heroicons/vue/24/outline'
</script>

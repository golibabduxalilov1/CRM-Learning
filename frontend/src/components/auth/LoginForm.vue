<template>
  <div class="relative overflow-hidden rounded-[28px] border border-slate-100/80 bg-white shadow-2xl shadow-primary-900/5">
    <div class="absolute -left-24 -top-24 h-56 w-56 rounded-full bg-primary-200/50 blur-3xl" />
    <div class="absolute -right-24 bottom-0 h-64 w-64 rounded-full bg-indigo-200/60 blur-3xl" />
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(59,130,246,0.08),transparent_35%)]" />

    <div class="relative p-8 sm:p-10 space-y-8">
      <header class="space-y-3">
        <div class="inline-flex items-center gap-2 rounded-full bg-primary-50 px-3 py-1 text-xs font-semibold text-primary-700 ring-1 ring-primary-100">
          <span class="h-2 w-2 rounded-full bg-primary-500 shadow-[0_0_0_4px_rgba(59,130,246,0.15)]" />
          {{ showOTP ? 'Ikki bosqichli tasdiq' : 'Qayta xush kelibsiz' }}
        </div>
        <div class="flex items-center justify-between gap-3">
          <div>
            <h2 class="text-3xl font-bold text-slate-900 tracking-tight">
              {{ showOTP ? 'OTP kodni kiriting' : 'Tizimga kirish' }}
            </h2>
            <p class="text-sm text-slate-500">
              {{ showOTP ? "Emailingizga yuborilgan 6 xonali kodni tasdiqlang." : "Email va parolni kiriting, so'ng OTP orqali tasdiqlang." }}
            </p>
          </div>
          <div class="hidden sm:flex h-12 w-12 items-center justify-center rounded-2xl bg-primary-50 text-primary-600 shadow-inner shadow-primary-100">
            <ShieldCheckIcon class="h-6 w-6" />
          </div>
        </div>
      </header>

      <form v-if="!showOTP" class="space-y-5" @submit.prevent="handleLogin">
        <div class="space-y-2">
          <label class="text-sm font-semibold text-slate-700">Email manzili</label>
          <div class="relative">
            <div class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
              <EnvelopeIcon class="h-5 w-5" />
            </div>
            <input
              v-model="form.email"
              type="email"
              required
              autocomplete="email"
              class="input-soft pl-12"
              placeholder="email@example.com"
            />
          </div>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-semibold text-slate-700">Parol</label>
          <div class="relative">
            <div class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
              <LockClosedIcon class="h-5 w-5" />
            </div>
            <input
              v-model="form.password"
              :type="passwordInputType"
              required
              autocomplete="current-password"
              class="input-soft pl-12 pr-12"
              placeholder="Kirish paroli"
            />
            <button
              type="button"
              class="absolute inset-y-2 right-2 flex items-center rounded-xl px-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-600 p-2 rounded-md"
              @click="togglePassword"
              aria-label="Parolni ko'rsatish"
            >
              <component :is="passwordVisible ? EyeSlashIcon : EyeIcon" class="h-5 w-5" />
            </button>
          </div>
          <div class="flex items-center justify-between text-xs text-slate-500">
            <span>Minimal 8 belgidan iborat parol kiriting.</span>
            <router-link to="/register" class="font-semibold text-primary-600 hover:text-primary-700">
              Ro'yxatdan o'tish
            </router-link>
          </div>
        </div>

        <transition name="fade">
          <div
            v-if="error"
            class="flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 shadow-sm"
          >
            <ExclamationTriangleIcon class="mt-0.5 h-5 w-5 flex-none" />
            <span>{{ error }}</span>
          </div>
        </transition>

        <button
          type="submit"
          :disabled="loading"
          class="btn-primary w-full justify-center rounded-2xl py-3 text-base font-semibold shadow-lg shadow-primary-500/30 hover:-translate-y-0.5 transition disabled:translate-y-0 disabled:opacity-70 p-2 rounded-md"
        >
          {{ loading ? 'Yuklanmoqda...' : 'Davom etish' }}
        </button>

        <div class="flex items-center gap-3 text-[13px] text-slate-500">
          <div class="h-px flex-1 bg-gradient-to-r from-transparent via-slate-200 to-transparent" />
          Ikki bosqichli autentifikatsiya bilan himoya qilingan
          <div class="h-px flex-1 bg-gradient-to-r from-transparent via-slate-200 to-transparent" />
        </div>
      </form>

      <form v-else class="space-y-6" @submit.prevent="handleVerifyOTP">
        <div class="grid gap-2 rounded-2xl border border-primary-100 bg-primary-50/60 p-4 text-sm text-primary-800 shadow-inner shadow-primary-100">
          <div class="flex items-center gap-2">
            <SparklesIcon class="h-5 w-5" />
            <p class="font-semibold">Tasdiqlash kodi yuborildi</p>
          </div>
          <p class="text-primary-700">
            {{ form.email }} manziliga 6 xonali kod jo'natildi. Kod 5 daqiqa ichida amal qiladi.
          </p>
        </div>

        <div class="space-y-2">
          <label class="text-sm font-semibold text-slate-700">OTP kod</label>
          <input
            v-model="otpCode"
            type="text"
            required
            maxlength="6"
            class="input-soft text-center text-2xl tracking-[0.5em] font-bold uppercase"
            placeholder="000000"
          />
          <p class="text-xs text-slate-500">Agar kod kelmasa, spam papkasini tekshiring.</p>
        </div>

        <transition name="fade">
          <div
            v-if="error"
            class="flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 shadow-sm"
          >
            <ExclamationTriangleIcon class="mt-0.5 h-5 w-5 flex-none" />
            <span>{{ error }}</span>
          </div>
        </transition>

        <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <button
            type="submit"
            :disabled="loading"
            class="btn-primary w-full justify-center rounded-2xl py-3 text-base font-semibold shadow-lg shadow-primary-500/30 hover:-translate-y-0.5 transition disabled:translate-y-0 disabled:opacity-70 sm:w-auto sm:px-6 p-2 rounded-md"
          >
            {{ loading ? 'Tekshirilmoqda...' : 'Tasdiqlash' }}
          </button>
          <button
            type="button"
            class="btn-secondary w-full justify-center rounded-2xl py-3 text-base font-semibold sm:w-auto sm:px-6 p-2 rounded-md"
            @click="resetStep"
          >
            Ortga qaytish
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAuthStore } from '@/store/modules/auth'
import { EyeIcon, EyeSlashIcon, EnvelopeIcon, LockClosedIcon, ShieldCheckIcon, SparklesIcon } from '@heroicons/vue/24/outline'
import { ExclamationTriangleIcon } from '@heroicons/vue/24/solid'

const authStore = useAuthStore()

const form = ref({
  email: '',
  password: '',
})

const otpCode = ref('')
const showOTP = ref(false)
const loading = ref(false)
const error = ref(null)
const passwordVisible = ref(false)

const passwordInputType = computed(() => (passwordVisible.value ? 'text' : 'password'))

const togglePassword = () => {
  passwordVisible.value = !passwordVisible.value
}

const resetStep = () => {
  showOTP.value = false
  otpCode.value = ''
  error.value = null
}

const handleLogin = async () => {
  loading.value = true
  error.value = null

  const result = await authStore.login(form.value)

  if (result.success) {
    showOTP.value = true
  } else {
    error.value = result.error?.detail || 'Login xatolik'
  }

  loading.value = false
}

const handleVerifyOTP = async () => {
  loading.value = true
  error.value = null

  const result = await authStore.verifyOTP({
    email: form.value.email,
    code: otpCode.value,
  })

  if (!result.success) {
    error.value = result.error?.detail || 'OTP tasdiqlash xatolik'
  }

  loading.value = false
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>

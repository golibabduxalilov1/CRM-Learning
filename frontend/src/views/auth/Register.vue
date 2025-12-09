<template>
  <section
    class="relative min-h-screen overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-primary-900 text-white"
  >
    <div class="absolute inset-0 opacity-50">
      <div
        class="absolute -top-24 -left-32 h-96 w-96 rounded-full bg-primary-500/30 blur-[120px]"
      />
      <div
        class="absolute bottom-0 right-0 h-[520px] w-[520px] rounded-full bg-indigo-500/25 blur-[140px]"
      />
      <div
        class="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(59,130,246,0.14),transparent_35%),radial-gradient(circle_at_80%_0%,rgba(99,102,241,0.12),transparent_30%),linear-gradient(120deg,rgba(255,255,255,0.04),transparent_40%)]"
      />
    </div>

    <div
      class="relative mx-auto grid max-w-6xl items-stretch gap-10 px-6 py-12 lg:grid-cols-2 lg:px-10"
    >
      <div
        class="glass-panel flex flex-col justify-between gap-8 rounded-[28px] p-10 text-white shadow-[0_24px_90px_rgba(15,23,42,0.35)]"
      >
        <div class="space-y-4">
          <div
            class="inline-flex items-center gap-3 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm font-semibold text-white/80"
          >
            <AcademicCapIcon class="h-6 w-6 text-primary-200" />
            Training CRM • Study Center Edition
          </div>
          <h1 class="text-4xl font-extrabold leading-tight">
            Jamoangiz uchun premium boshqaruv paneli
          </h1>
          <p class="text-lg text-slate-200/80">
            Ro'yxatdan o'ting va rollarga moslangan kirish, real-time ko'rsatkichlar hamda xavfsiz
            to'lov monitoringidan foydalaning.
          </p>
        </div>

        <div class="grid gap-4 sm:grid-cols-2">
          <div
            class="flex items-start gap-3 rounded-2xl bg-white/5 p-4 backdrop-blur border border-white/10"
          >
            <CheckBadgeIcon class="mt-1 h-6 w-6 text-primary-200" />
            <div class="space-y-1">
              <p class="font-semibold">Rolga asoslangan ruxsatlar</p>
              <p class="text-sm text-slate-200/70">
                SUPERADMIN, BOSS, ADMIN va MENTOR uchun alohida panel.
              </p>
            </div>
          </div>
          <div
            class="flex items-start gap-3 rounded-2xl bg-white/5 p-4 backdrop-blur border border-white/10"
          >
            <ChartBarIcon class="mt-1 h-6 w-6 text-primary-200" />
            <div class="space-y-1">
              <p class="font-semibold">Real-time analitika</p>
              <p class="text-sm text-slate-200/70">
                To'lovlar, guruhlar va talabalar statistikasi.
              </p>
            </div>
          </div>
          <div
            class="flex items-start gap-3 rounded-2xl bg-white/5 p-4 backdrop-blur border border-white/10 sm:col-span-2"
          >
            <ShieldCheckIcon class="mt-1 h-6 w-6 text-primary-200" />
            <div class="space-y-1">
              <p class="font-semibold">Ikki bosqichli autentifikatsiya</p>
              <p class="text-sm text-slate-200/70">
                OTP bilan himoyalangan kirish va barqaror xavfsizlik.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="relative">
        <div
          class="absolute inset-0 -left-6 top-6 rounded-[32px] bg-gradient-to-br from-primary-500/20 via-indigo-400/10 to-transparent blur-2xl"
        />
        <div
          class="relative overflow-hidden rounded-[28px] border border-slate-100/80 bg-white shadow-2xl shadow-primary-900/5"
        >
          <div
            class="absolute -left-24 -top-24 h-56 w-56 rounded-full bg-primary-200/50 blur-3xl"
          />
          <div
            class="absolute -right-24 bottom-0 h-64 w-64 rounded-full bg-indigo-200/60 blur-3xl"
          />
          <div
            class="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(59,130,246,0.08),transparent_35%)]"
          />

          <div class="relative p-8 sm:p-10">
            <div class="space-y-2">
              <p class="text-sm font-semibold uppercase tracking-[0.3em] text-primary-600">
                Create account
              </p>
              <h2 class="text-3xl font-bold text-slate-900">Ro'yxatdan o'tish</h2>
              <p class="text-slate-500">Ma'lumotlaringizni kiriting va jamoangizga qo'shiling.</p>
            </div>

            <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
              <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div class="space-y-2">
                  <label class="text-sm font-medium text-slate-700">Ism</label>
                  <input
                    v-model="form.first_name"
                    type="text"
                    required
                    class="input-soft"
                    placeholder="Dilshod"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-sm font-medium text-slate-700">Familiya</label>
                  <input
                    v-model="form.last_name"
                    type="text"
                    required
                    class="input-soft"
                    placeholder="Karimov"
                  />
                </div>
              </div>

              <div class="space-y-2">
                <label class="text-sm font-medium text-slate-700">Email</label>
                <input
                  v-model="form.email"
                  type="email"
                  required
                  class="input-soft"
                  placeholder="you@example.com"
                />
              </div>

              <div class="space-y-2">
                <label class="text-sm font-medium text-slate-700">Telefon</label>
                <input
                  v-model="form.phone"
                  type="tel"
                  class="input-soft"
                  placeholder="+998 90 123 45 67"
                />
              </div>

              <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div class="space-y-2">
                  <label class="text-sm font-medium text-slate-700">Parol</label>
                  <input
                    v-model="form.password"
                    type="password"
                    required
                    minlength="6"
                    autocomplete="new-password"
                    class="input-soft"
                    placeholder="••••••••"
                  />
                </div>
                <div class="space-y-2">
                  <label class="text-sm font-medium text-slate-700">Parolni tasdiqlang</label>
                  <input
                    v-model="form.password_confirm"
                    type="password"
                    required
                    minlength="6"
                    autocomplete="new-password"
                    class="input-soft"
                    placeholder="••••••••"
                  />
                </div>
              </div>

              <div
                v-if="error"
                class="flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 shadow-sm"
              >
                {{ error }}
              </div>

              <button
                type="submit"
                class="btn-primary w-full justify-center py-3 text-base font-semibold shadow-lg shadow-primary-500/30 hover:-translate-y-0.5 transition disabled:translate-y-0 disabled:opacity-70 p-2 rounded-md"
                :disabled="loading"
              >
                {{ loading ? "Ro'yxatdan o'tilmoqda..." : "Ro'yxatdan o'tish" }}
              </button>
            </form>

            <p class="mt-8 text-center text-sm text-slate-600">
              Akkauntingiz bormi?
              <router-link
                to="/login"
                class="font-semibold text-primary-600 hover:text-primary-700"
              >
                Tizimga kirish
              </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth'
import { useNotification } from '@/composables/useNotification'
import {
  AcademicCapIcon,
  CheckBadgeIcon,
  ChartBarIcon,
  ShieldCheckIcon,
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const { showSuccess, showError } = useNotification()

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  password: '',
  password_confirm: '',
})

const loading = ref(false)
const error = ref('')

const extractErrorMessage = (err) => {
  if (!err) return "Ro'yxatdan o'tishda xatolik yuz berdi"

  if (typeof err === 'string') {
    return err
  }

  if (Array.isArray(err)) {
    return err[0]
  }

  if (typeof err === 'object') {
    const firstKey = Object.keys(err)[0]
    const value = err[firstKey]
    if (Array.isArray(value)) {
      return value[0]
    }
    if (typeof value === 'string') {
      return value
    }
  }

  return "Ro'yxatdan o'tishda xatolik yuz berdi"
}

const handleSubmit = async () => {
  if (form.value.password !== form.value.password_confirm) {
    error.value = 'Parollar mos kelmadi'
    return
  }

  loading.value = true
  error.value = ''

  const result = await authStore.register({
    first_name: form.value.first_name,
    last_name: form.value.last_name,
    email: form.value.email,
    phone: form.value.phone,
    password: form.value.password,
    password_confirm: form.value.password_confirm,
  })

  if (result.success) {
    showSuccess("Ro'yxatdan o'tish muvaffaqiyatli yakunlandi. Endi tizimga kiring.")
    router.push('/login')
  } else {
    const detail = result.error?.detail || extractErrorMessage(result.error)
    error.value = detail
    showError(detail)
  }

  loading.value = false
}
</script>

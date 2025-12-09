<template>
  <div class="relative flex min-h-screen bg-slate-50">
    <Sidebar class="relative z-10" />
    <div class="relative z-0 flex-1 overflow-y-auto">
      <div
        class="absolute inset-x-0 top-0 h-80 bg-gradient-to-br from-primary-600 via-primary-700 to-indigo-800 p-8 text-white shadow-xl shadow-primary-900/20"
      >
        <div class="absolute inset-0 opacity-60">
          <div
            class="absolute -top-20 -left-28 h-80 w-80 rounded-full bg-primary-500/30 blur-[120px]"
          />
          <div
            class="absolute bottom-0 right-0 h-96 w-96 rounded-full bg-indigo-500/25 blur-[140px]"
          />
          <div
            class="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(59,130,246,0.18),transparent_35%),radial-gradient(circle_at_80%_0%,rgba(99,102,241,0.12),transparent_30%),linear-gradient(120deg,rgba(255,255,255,0.06),transparent_40%)]"
          />
        </div>
      </div>

      <div class="relative px-4 py-6 space-y-8 lg:px-10 lg:py-12">
        <!-- Hero -->
        <section
          class="glass-panel rounded-3xl border-white/10 bg-white/10 p-6 text-white shadow-2xl shadow-primary-900/30 lg:p-8"
        >
          <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div class="flex items-center gap-4">
              <div
                class="flex h-16 w-16 items-center justify-center rounded-full bg-white/20 text-2xl font-semibold mb-4"
              >
                {{ avatarInitials }}
              </div>
              <div>
                <p class="text-xs font-semibold uppercase tracking-[0.3em] text-white/70">
                  {{ heroGreeting }}
                </p>
                <h1 class="text-3xl font-bold tracking-tight">
                  {{ fullName || 'Profil Sozlamalari' }}
                </h1>
                <p class="mt-2 text-sm text-white/80">
                  {{ heroSubtitle }}
                </p>
              </div>
            </div>

            <div class="w-full max-w-md space-y-3">
              <div
                class="flex items-center justify-between text-xs font-semibold uppercase tracking-wide text-white/80"
              >
                <span>Profil to'ldirilgan</span>
                <span>{{ profileCompleteness }}%</span>
              </div>
              <div class="h-3 rounded-full bg-white/15">
                <div
                  class="h-3 rounded-full bg-gradient-to-r from-primary-200 to-white shadow-lg shadow-white/40 transition-all"
                  :style="{ width: `${profileCompleteness}%` }"
                ></div>
              </div>
              <div class="flex flex-wrap gap-3 text-xs font-medium text-white/80">
                <span
                  v-for="chip in heroChips"
                  :key="chip.label"
                  class="pill-soft border-white/20 bg-white/10"
                >
                  {{ chip.label }}: {{ chip.value }}
                </span>
              </div>
            </div>
          </div>
        </section>

        <section class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <div
            v-for="stat in statCards"
            :key="stat.label"
            class="card-flat flex items-start gap-3 bg-white"
          >
            <div
              class="rounded-2xl bg-primary-50 p-2 text-primary-600 shadow-inner shadow-primary-100/60"
            >
              <component :is="stat.icon" class="h-5 w-5" />
            </div>
            <div>
              <p class="text-[11px] font-semibold uppercase tracking-[0.2em] text-slate-500">
                {{ stat.label }}
              </p>
              <p class="text-xl font-bold text-slate-900">{{ stat.value }}</p>
              <p class="text-xs text-slate-500">{{ stat.caption }}</p>
            </div>
          </div>
        </section>

        <!-- Forms -->
        <section class="grid gap-6 lg:grid-cols-2">
          <div class="card glass-panel p-4">
            <div class="mb-6 flex items-center justify-between">
              <div>
                <h2 class="text-xl font-semibold text-slate-900">Shaxsiy ma'lumotlar</h2>
                <p class="text-sm text-slate-500">
                  Profilingizni yangilang va kontaktlaringizni tekshiring.
                </p>
              </div>
            </div>

            <form class="space-y-6" @submit.prevent="handleUpdateProfile">
              <div class="grid gap-5 md:grid-cols-2">
                <div class="space-y-2">
                  <div
                    class="input-label flex items-center justify-between text-sm font-semibold text-slate-600"
                  >
                    <span>Ism</span>
                    <span
                      :class="[
                        'status-pill',
                        getFieldStatus('first_name').complete ? 'success' : 'warning',
                      ]"
                    >
                      {{ getFieldStatus('first_name').text }}
                    </span>
                  </div>
                  <div class="input-shell">
                    <UserCircleIcon class="input-icon" />
                    <input
                      v-model="profileForm.first_name"
                      type="text"
                      placeholder="Ismingiz"
                      spellcheck="false"
                      autocomplete="off"
                      class="flex-1 border-0 bg-transparent p-0 focus:ring-0"
                    />
                  </div>
                  <p class="input-hint">Rasmiy hujjatlardagi kabi kiriting.</p>
                </div>

                <div class="space-y-2">
                  <div
                    class="input-label flex items-center justify-between text-sm font-semibold text-slate-600"
                  >
                    <span>Familiya</span>
                    <span
                      :class="[
                        'status-pill',
                        getFieldStatus('last_name').complete ? 'success' : 'warning',
                      ]"
                    >
                      {{ getFieldStatus('last_name').text }}
                    </span>
                  </div>
                  <div class="input-shell">
                    <UserCircleIcon class="input-icon" />
                    <input
                      v-model="profileForm.last_name"
                      type="text"
                      placeholder="Familiyangiz"
                      spellcheck="false"
                      autocomplete="off"
                      class="flex-1 border-0 bg-transparent p-0 focus:ring-0"
                    />
                  </div>
                  <p class="input-hint">Diplom va shartnomalarda ko'rsatilgan familiya.</p>
                </div>
              </div>

              <div class="space-y-2">
                <div
                  class="input-label flex items-center justify-between text-sm font-semibold text-slate-600"
                >
                  <span>Email</span>
                  <span class="status-pill neutral">Tizim boshqaradi</span>
                </div>
                <div class="input-shell bg-slate-50">
                  <EnvelopeIcon class="input-icon" />
                  <input
                    v-model="profileForm.email"
                    type="email"
                    disabled
                    class="flex-1 border-0 bg-transparent p-0 cursor-not-allowed text-slate-500 focus:ring-0"
                    placeholder="email@example.com"
                  />
                </div>
                <p class="input-hint">Email manzilini administrator o'zgartirishi mumkin.</p>
              </div>

              <div class="space-y-2">
                <div
                  class="input-label flex items-center justify-between text-sm font-semibold text-slate-600"
                >
                  <span>Telefon</span>
                  <span
                    :class="[
                      'status-pill',
                      getFieldStatus('phone').complete ? 'success' : 'warning',
                    ]"
                  >
                    {{ getFieldStatus('phone').text }}
                  </span>
                </div>
                <div class="input-shell">
                  <DevicePhoneMobileIcon class="input-icon" />
                  <input
                    v-model="profileForm.phone"
                    type="tel"
                    placeholder="+998 (__) ___-__-__"
                    spellcheck="false"
                    autocomplete="off"
                    class="flex-1 border-0 bg-transparent p-0 focus:ring-0"
                  />
                </div>
                <p class="input-hint">SMS eslatmalar va bog'lanish uchun ishlatiladi.</p>
              </div>

              <div class="flex flex-wrap gap-3">
                <button type="submit" :disabled="loading" class="btn-primary p-2 rounded-md">
                  {{ loading ? 'Saqlanmoqda...' : "Ma'lumotlarni saqlash" }}
                </button>
                <button
                  type="button"
                  class="btn-secondary p-2 rounded-md"
                  @click="resetProfileForm"
                  :disabled="loading"
                >
                  Bekor qilish
                </button>
              </div>
            </form>
          </div>

          <div class="card glass-panel p-4">
            <div class="mb-6">
              <h2 class="text-xl font-semibold text-slate-900">Parolni o'zgartirish</h2>
              <p class="text-sm text-slate-500">
                Hisobingizni himoya qilish uchun parolingizni vaqti-vaqti bilan yangilang.
              </p>
            </div>

            <form class="space-y-6" @submit.prevent="handleChangePassword">
              <div class="space-y-2">
                <div
                  class="input-label flex items-center justify-between text-sm font-semibold text-slate-600"
                >
                  <span>Joriy parol</span>
                  <span class="status-pill neutral">Maxfiy</span>
                </div>
                <div class="input-shell">
                  <LockClosedIcon class="input-icon" />
                  <input
                    v-model="passwordForm.old_password"
                    type="password"
                    placeholder="••••••••"
                    autocomplete="current-password"
                    class="flex-1 border-0 bg-transparent p-0 focus:ring-0"
                  />
                </div>
                <p class="input-hint">Tizimga oxirgi kirishda ishlatgan parolingiz.</p>
              </div>

              <div class="space-y-3">
                <div
                  class="input-label flex items-center justify-between text-sm font-semibold text-slate-600"
                >
                  <span>Yangi parol</span>
                  <span :class="['status-pill', passwordStrength.className]">{{
                    passwordStrength.label
                  }}</span>
                </div>
                <div class="input-shell">
                  <LockClosedIcon class="input-icon" />
                  <input
                    v-model="passwordForm.new_password"
                    type="password"
                    placeholder="Kamida 8 ta belgi"
                    autocomplete="new-password"
                    class="flex-1 border-0 bg-transparent p-0 focus:ring-0"
                  />
                </div>
                <div class="progress-track">
                  <div
                    class="progress-bar"
                    :style="{
                      width: `${passwordStrength.percent}%`,
                      backgroundColor: passwordStrength.color,
                    }"
                  ></div>
                </div>
                <p class="input-hint">
                  Murakkab parol hisobingiz uchun qo'shimcha xavfsizlik beradi.
                </p>
              </div>

              <div class="space-y-2">
                <div
                  class="input-label flex items-center justify-between text-sm font-semibold text-slate-600"
                >
                  <span>Yangi parolni tasdiqlang</span>
                  <span
                    :class="[
                      'status-pill',
                      passwordMatch === null ? 'neutral' : passwordMatch ? 'success' : 'warning',
                    ]"
                  >
                    {{
                      passwordMatch === null ? 'Kiritilmagan' : passwordMatch ? 'Mos' : 'Mos emas'
                    }}
                  </span>
                </div>
                <div class="input-shell">
                  <KeyIcon class="input-icon" />
                  <input
                    v-model="passwordForm.confirm_password"
                    type="password"
                    placeholder="Parolni takrorlang"
                    autocomplete="new-password"
                    class="flex-1 border-0 bg-transparent p-0 focus:ring-0"
                  />
                </div>
                <p class="input-hint">Parolni aynan shu shaklda takrorlang.</p>
              </div>

              <ul class="space-y-2 text-sm">
                <li
                  v-for="req in passwordRequirements"
                  :key="req.label"
                  class="flex items-center gap-2"
                  :class="req.met ? 'text-success-600' : 'text-slate-500'"
                >
                  <CheckCircleIcon v-if="req.met" class="h-4 w-4" />
                  <ExclamationTriangleIcon v-else class="h-4 w-4 text-warning-500" />
                  <span>{{ req.label }}</span>
                </li>
              </ul>

              <div class="flex flex-wrap gap-3">
                <button
                  type="submit"
                  :disabled="loadingPassword"
                  class="btn-primary p-2 rounded-md"
                >
                  {{ loadingPassword ? "O'zgartirilmoqda..." : "Parolni o'zgartirish" }}
                </button>
                <button
                  type="button"
                  class="btn-secondary p-2 rounded-md"
                  @click="resetPasswordForm"
                  :disabled="loadingPassword"
                >
                  Tozalash
                </button>
              </div>
            </form>
          </div>
        </section>

        <!-- Account insights -->
        <section class="grid gap-6 lg:grid-cols-3">
          <div class="card lg:col-span-2 p-4">
            <h2 class="text-xl font-semibold text-slate-900">Akkaunt ma'lumotlari</h2>
            <p class="text-sm text-slate-500">Profilingiz haqidagi umumiy ma'lumotlar.</p>

            <dl class="mt-6 grid gap-4 sm:grid-cols-2">
              <div class="rounded-2xl border border-slate-100 bg-slate-50/70 p-4">
                <dt class="text-xs font-semibold uppercase tracking-wide text-slate-500">Rol</dt>
                <dd class="mt-2 text-base font-semibold text-slate-900">{{ userRoleLabel }}</dd>
              </div>
              <div class="rounded-2xl border border-slate-100 bg-slate-50/70 p-4">
                <dt class="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Ro'yxatdan o'tgan sana
                </dt>
                <dd class="mt-2 text-base font-semibold text-slate-900">
                  {{ accountTimeline.joined || '-' }}
                </dd>
              </div>
              <div class="rounded-2xl border border-slate-100 bg-slate-50/70 p-4">
                <dt class="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Oxirgi kirish
                </dt>
                <dd class="mt-2 text-base font-semibold text-slate-900">
                  {{ accountTimeline.lastLogin || '-' }}
                </dd>
              </div>
              <div class="rounded-2xl border border-slate-100 bg-slate-50/70 p-4">
                <dt class="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Bog'langan telefon
                </dt>
                <dd class="mt-2 text-base font-semibold text-slate-900">{{ contactPhone }}</dd>
              </div>
            </dl>
          </div>

          <div class="card p-4">
            <h2 class="text-xl font-semibold text-slate-900">Xavfsizlik nazorati</h2>
            <p class="text-sm text-slate-500">Profilni to'liqroq himoya qilish uchun tavsiyalar.</p>

            <ul class="mt-5 space-y-4">
              <li
                v-for="tip in profileTips"
                :key="tip.title"
                class="flex items-start gap-3 rounded-2xl border border-slate-100 bg-slate-50/70 p-4"
              >
                <div
                  class="mt-1 h-3 w-3 rounded-full"
                  :class="tip.complete ? 'bg-success-500' : 'bg-warning-500'"
                ></div>
                <div>
                  <p class="font-semibold text-slate-900">{{ tip.title }}</p>
                  <p class="text-sm text-slate-500">{{ tip.description }}</p>
                  <p
                    class="mt-1 text-xs font-medium"
                    :class="tip.complete ? 'text-success-600' : 'text-warning-600'"
                  >
                    {{ tip.complete ? 'Bajarildi' : 'Harakat talab qilinadi' }}
                  </p>
                </div>
              </li>
            </ul>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '@/store/modules/auth'
import { useNotification } from '@/composables/useNotification'
import Sidebar from '@/components/common/Sidebar.vue'
import authService from '@/services/auth.service'
import { formatDate, formatDateTime, getRoleLabel } from '@/utils/helpers'
import {
  UserCircleIcon,
  EnvelopeIcon,
  DevicePhoneMobileIcon,
  ClockIcon,
  LockClosedIcon,
  KeyIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const { showSuccess, showError } = useNotification()

const profileForm = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
})

const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

const loading = ref(false)
const loadingPassword = ref(false)

const syncProfileForm = () => {
  if (!authStore.user) return
  profileForm.value = {
    first_name: authStore.user.first_name || '',
    last_name: authStore.user.last_name || '',
    email: authStore.user.email || '',
    phone: authStore.user.phone || '',
  }
}

watch(
  () => authStore.user,
  () => {
    syncProfileForm()
  },
  { immediate: true },
)

const fullName = computed(() => {
  if (!authStore.user) return ''
  return `${authStore.user.first_name || ''} ${authStore.user.last_name || ''}`.trim()
})

const avatarInitials = computed(() => {
  if (!authStore.user) return '??'
  const first = authStore.user.first_name?.[0] ?? ''
  const last = authStore.user.last_name?.[0] ?? ''
  const initials = `${first}${last}`.trim()
  return initials ? initials.toUpperCase() : '??'
})

const heroGreeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Xayrli tong'
  if (hour < 18) return 'Kun davomida'
  return 'Kechgi smena'
})

const heroSubtitle = computed(
  () =>
    `Hurmatli ${getRoleLabel(authStore.user?.role) || 'foydalanuvchi'}, profilingizni boshqarish uchun barcha imkoniyatlar bir joyda.`,
)

const userRoleLabel = computed(() => getRoleLabel(authStore.user?.role) || 'Noma’lum rol')

const accountTimeline = computed(() => ({
  joined: formatDate(authStore.user?.created_at),
  lastLogin: formatDateTime(authStore.user?.last_login),
}))

const contactPhone = computed(() => profileForm.value.phone || 'Kiritilmagan')

const fieldStatus = computed(() => {
  const resolve = (value, fallback = 'Talab qilinadi') =>
    value ? { text: "To'ldirilgan", complete: true } : { text: fallback, complete: false }
  return {
    first_name: resolve(profileForm.value.first_name),
    last_name: resolve(profileForm.value.last_name),
    phone: resolve(profileForm.value.phone, 'Telefon talab qilinadi'),
  }
})

const getFieldStatus = (field) => fieldStatus.value[field] || { text: '', complete: false }

const profileCompleteness = computed(() => {
  const fields = ['first_name', 'last_name', 'phone']
  const filled = fields.filter((field) => !!profileForm.value[field]).length
  return Math.min(100, Math.max(35, Math.round((filled / fields.length) * 100)))
})

const heroChips = computed(() => [
  { label: 'Rol', value: userRoleLabel.value },
  { label: "Ro'yxatdan o'tgan", value: accountTimeline.value.joined || '-' },
  { label: 'Oxirgi kirish', value: accountTimeline.value.lastLogin || '-' },
])

const statCards = computed(() => [
  {
    label: 'Profil',
    value: fullName.value || 'Ism kiritilmagan',
    caption: userRoleLabel.value,
    icon: UserCircleIcon,
  },
  {
    label: 'Email',
    value: profileForm.value.email || '-',
    caption: 'Asosiy kontakt',
    icon: EnvelopeIcon,
  },
  {
    label: 'Telefon',
    value: contactPhone.value,
    caption: "SMS va bog'lanish uchun",
    icon: DevicePhoneMobileIcon,
  },
  {
    label: "So'nggi faoliyat",
    value: accountTimeline.value.lastLogin || 'Hali kirilmagan',
    caption: 'Kuzatuv',
    icon: ClockIcon,
  },
])

const profileTips = computed(() => [
  {
    title: 'Telefon raqami',
    description:
      contactPhone.value === 'Kiritilmagan'
        ? 'SMS ogohlantirishlar uchun telefon raqamingizni kiriting.'
        : 'Telefon raqamingiz yangilangan.',
    complete: contactPhone.value !== 'Kiritilmagan',
  },
  {
    title: 'Parolni yangilab turing',
    description: "Har 90 kunda parolni o'zgartirish tavsiya etiladi.",
    complete: false,
  },
  {
    title: "Profil ma'lumotlari",
    description:
      profileCompleteness.value === 100
        ? "Barcha kerakli maydonlar to'ldirilgan."
        : "Ism, familiya va telefonni to'ldiring.",
    complete: profileCompleteness.value === 100,
  },
])

const passwordRequirements = computed(() => [
  { label: 'Kamida 8 ta belgi', met: passwordForm.value.new_password.length >= 8 },
  { label: 'Biror raqam ishlatilgan', met: /\d/.test(passwordForm.value.new_password) },
  { label: 'Katta harf mavjud', met: /[A-Z]/.test(passwordForm.value.new_password) },
  { label: 'Maxsus belgi ishlatilgan', met: /[^A-Za-z0-9]/.test(passwordForm.value.new_password) },
])

const passwordStrength = computed(() => {
  const total = passwordRequirements.value.length
  const met = passwordRequirements.value.filter((req) => req.met).length
  const percent = total ? Math.round((met / total) * 100) : 0

  if (!passwordForm.value.new_password) {
    return { percent: 0, label: 'Kiritilmagan', className: 'neutral', color: '#94a3b8' }
  }

  if (percent <= 50) {
    return { percent, label: 'Zaif', className: 'warning', color: '#f97316' }
  }

  if (percent < 100) {
    return { percent, label: "O'rtacha", className: 'warning', color: '#f59e0b' }
  }

  return { percent, label: 'Kuchli', className: 'success', color: '#16a34a' }
})

const passwordMatch = computed(() => {
  if (!passwordForm.value.confirm_password) return null
  return passwordForm.value.new_password === passwordForm.value.confirm_password
})

const resetProfileForm = () => {
  syncProfileForm()
}

const resetPasswordForm = () => {
  passwordForm.value = {
    old_password: '',
    new_password: '',
    confirm_password: '',
  }
}

const handleUpdateProfile = async () => {
  loading.value = true
  try {
    await authService.updateProfile(profileForm.value)
    await authStore.fetchCurrentUser({ force: true })
    showSuccess('Profil muvaffaqiyatli yangilandi')
  } catch (error) {
    showError('Profilni yangilashda xatolik')
  } finally {
    loading.value = false
  }
}

const handleChangePassword = async () => {
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    showError('Parollar mos kelmaydi')
    return
  }

  loadingPassword.value = true
  try {
    await authService.changePassword({
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password,
    })
    resetPasswordForm()
    showSuccess("Parol muvaffaqiyatli o'zgartirildi")
  } catch (error) {
    showError("Parolni o'zgartirishda xatolik")
  } finally {
    loadingPassword.value = false
  }
}
</script>

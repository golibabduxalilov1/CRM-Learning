<template>
  <section
    class="relative min-h-screen overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-primary-900 text-white"
  >
    <div class="absolute inset-0 opacity-50">
      <div
        class="absolute -top-24 -left-24 h-72 w-72 rounded-full bg-primary-500/30 blur-[120px]"
      />
      <div
        class="absolute bottom-10 right-0 h-96 w-96 rounded-full bg-indigo-500/25 blur-[140px]"
      />
      <div
        class="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(59,130,246,0.12),transparent_35%),radial-gradient(circle_at_80%_0%,rgba(99,102,241,0.12),transparent_30%),linear-gradient(120deg,rgba(255,255,255,0.06),transparent_40%)]"
      />
    </div>

    <div
      class="relative mx-auto flex min-h-screen max-w-6xl flex-col justify-center gap-12 px-6 py-14 lg:flex-row lg:items-center lg:px-10"
    >
      <div class="flex-1 space-y-8">
        <div
          class="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm font-semibold text-white/80 backdrop-blur"
        >
          <SparklesIcon class="h-5 w-5 text-primary-200" />
          Training CRM • Study Center Edition
        </div>

        <div class="space-y-4">
          <h1 class="text-5xl font-black leading-tight tracking-tight sm:text-6xl">
            O'quv markazingiz uchun
            <span class="text-primary-200">premium boshqaruv</span>
          </h1>
        </div>

        <div class="flex flex-col gap-4 sm:flex-row sm:items-center">
          <router-link
            to="/login"
            class="group inline-flex items-center justify-center gap-2 rounded-2xl bg-primary-600 px-8 py-4 text-lg font-semibold text-white shadow-xl shadow-primary-500/30 transition hover:-translate-y-0.5 hover:bg-primary-500"
          >
            <ArrowRightOnRectangleIcon class="h-6 w-6" />
            Tizimga kirish
          </router-link>
          <router-link
            to="/register"
            class="inline-flex items-center justify-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-8 py-4 text-lg font-semibold text-white backdrop-blur transition hover:-translate-y-0.5 hover:border-white/30"
          >
            <UserPlusIcon class="h-6 w-6" />
            Ro'yxatdan o'tish
          </router-link>
        </div>
      </div>

      <div class="flex-1">
        <div
          class="glass-panel grid gap-4 rounded-[28px] bg-white/5 p-8 shadow-[0_24px_90px_rgba(15,23,42,0.35)] backdrop-blur"
        >
          <div class="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 p-4">
            <AcademicCapIcon class="h-10 w-10 text-primary-200" />
            <div>
              <p class="text-xl font-semibold">Training CRM</p>
              <p class="text-sm text-slate-200/70">O'quv jarayonlarini raqamlashtiring</p>
            </div>
          </div>

          <div class="grid gap-3">
            <div
              class="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3 border border-white/10"
            >
              <div class="flex items-center gap-3">
                <UserGroupIcon class="h-6 w-6 text-primary-200" />
                <div>
                  <p class="font-semibold">Guruh va talabalar</p>
                  <p class="text-xs text-slate-200/70">Ro'yxat, dars jadvali va davomati.</p>
                </div>
              </div>
              <div
                class="rounded-full bg-primary-500/20 px-3 py-1 text-xs font-semibold text-primary-100"
              >
                Real-time
              </div>
            </div>

            <div
              class="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3 border border-white/10"
            >
              <div class="flex items-center gap-3">
                <CurrencyDollarIcon class="h-6 w-6 text-primary-200" />
                <div>
                  <p class="font-semibold">To'lovlar va payoutlar</p>
                  <p class="text-xs text-slate-200/70">Monitoring va mentor ulushlari.</p>
                </div>
              </div>
              <div
                class="rounded-full bg-emerald-500/20 px-3 py-1 text-xs font-semibold text-emerald-100"
              >
                Avtomatik
              </div>
            </div>

            <div
              class="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3 border border-white/10"
            >
              <div class="flex items-center gap-3">
                <ShieldCheckIcon class="h-6 w-6 text-primary-200" />
                <div>
                  <p class="font-semibold">Xavfsiz autentifikatsiya</p>
                  <p class="text-xs text-slate-200/70">OTP va email allowlist himoyasi.</p>
                </div>
              </div>
              <div
                class="rounded-full bg-indigo-500/20 px-3 py-1 text-xs font-semibold text-indigo-100"
              >
                OTP
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import {
  AcademicCapIcon,
  UserGroupIcon,
  CurrencyDollarIcon,
  ChartBarIcon,
  BellIcon,
  ShieldCheckIcon,
  ArrowRightOnRectangleIcon,
  UserPlusIcon,
  SparklesIcon,
} from '@heroicons/vue/24/outline'
</script>

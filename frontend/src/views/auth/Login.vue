<template>
  <section
    class="relative min-h-screen overflow-hidden bg-gradient-to-br from-slate-950 via-slate-900 to-primary-900 text-white"
  >
    <div class="absolute inset-0 opacity-40">
      <div
        class="absolute -top-32 -left-28 h-96 w-96 rounded-full bg-primary-500/40 blur-[120px]"
      />
      <div
        class="absolute bottom-0 right-0 h-[520px] w-[520px] rounded-full bg-indigo-500/30 blur-[140px]"
      />
      <div
        class="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(255,255,255,0.08),transparent_30%),radial-gradient(circle_at_80%_0%,rgba(99,102,241,0.12),transparent_30%),linear-gradient(120deg,rgba(255,255,255,0.04),transparent_40%)]"
      />
    </div>

    <div
      class="relative mx-auto grid min-h-screen max-w-6xl items-center gap-10 px-6 py-12 lg:grid-cols-2 lg:px-10"
    >
      <div class="space-y-10">
        <div
          class="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm font-semibold text-white/80 backdrop-blur"
        >
          <SparklesIcon class="h-5 w-5 text-primary-200" />
          Premium darajadagi o'quv markaz CRM
        </div>

        <div class="space-y-4">
          <p class="text-5xl font-extrabold leading-tight tracking-tight">
            Ma'lumotlar, to'lovlar va jamoa <span class="text-primary-200">bir ekranda</span>
          </p>
        </div>

        <div class="flex items-center gap-6">
          <div class="flex items-center gap-3">
            <div
              class="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/10 backdrop-blur"
            >
              <AcademicCapIcon class="h-7 w-7 text-primary-100" />
            </div>
            <div>
              <p class="text-sm text-slate-200/70">Training CRM</p>
              <p class="text-lg font-semibold">Study Center Edition</p>
            </div>
          </div>
        </div>
      </div>

      <div class="relative">
        <div
          class="absolute inset-0 -left-6 top-6 rounded-[32px] bg-gradient-to-br from-primary-500/20 via-indigo-400/10 to-transparent blur-2xl"
        />
        <LoginForm />
      </div>
    </div>
  </section>
</template>

<script setup>
import LoginForm from '@/components/auth/LoginForm.vue'
import {
  AcademicCapIcon,
  ChartBarIcon,
  ClockIcon,
  ShieldCheckIcon,
  SparklesIcon,
} from '@heroicons/vue/24/outline'
</script>

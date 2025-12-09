<template>
  <div class="flex min-h-screen bg-slate-50">
    <Sidebar />
    <div class="flex-1 flex flex-col min-w-0">
      <Navbar />
      <main class="flex-1 px-4 py-8 lg:px-8 space-y-6">
        <!-- Header -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button
              class="p-2 rounded-xl hover:bg-white hover:shadow-sm transition-all text-slate-500 hover:text-slate-700 rounded-md"
              @click="$router.back()"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            <div>
              <h1 class="text-2xl font-bold text-slate-800">Talaba ma'lumotlari</h1>
              <p class="text-sm text-slate-500">To'liq profil va tarix</p>
            </div>
          </div>
          <div class="flex gap-3" v-if="!isMentor">
            <button class="btn-secondary flex items-center gap-2 p-2 rounded-md">
              <PencilIcon class="w-4 h-4" />
              Tahrirlash
            </button>
          </div>
        </div>

        <div v-if="studentStore.loading" class="flex justify-center py-12">
          <Loading text="Ma'lumot yuklanmoqda..." />
        </div>

        <div v-else-if="studentStore.currentStudent" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Main Info Card -->
          <div class="lg:col-span-2 space-y-6">
            <div class="glass-panel p-6 relative overflow-hidden">
              <div class="absolute top-0 right-0 p-4 opacity-10">
                <UserIcon class="w-32 h-32 text-primary-500" />
              </div>
              
              <div class="relative z-10 flex items-start gap-6">
                <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center text-primary-600 text-2xl font-bold shadow-inner">
                  {{ student.first_name?.[0] }}{{ student.last_name?.[0] }}
                </div>
                <div class="flex-1">
                  <h2 class="text-2xl font-bold text-slate-800 mb-1">{{ student.full_name }}</h2>
                  <div class="flex items-center gap-3 text-sm text-slate-500 mb-4">
                    <span class="flex items-center gap-1">
                      <PhoneIcon class="w-4 h-4" />
                      {{ student.phone || '-' }}
                    </span>
                    <span class="w-1 h-1 rounded-full bg-slate-300"></span>
                    <span class="flex items-center gap-1">
                      <EnvelopeIcon class="w-4 h-4" />
                      {{ student.email || '-' }}
                    </span>
                  </div>
                  
                  <div class="flex gap-2">
                    <span 
                      class="px-3 py-1 rounded-full text-xs font-medium border"
                      :class="student.is_active 
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-100' 
                        : 'bg-rose-50 text-rose-700 border-rose-100'"
                    >
                      {{ student.is_active ? 'Faol' : "Nofaol" }}
                    </span>
                    <span class="px-3 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-600 border border-slate-200">
                      ID: #{{ student.id }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Additional Info -->
            <div class="bg-white rounded-2xl border border-slate-100 p-6 shadow-sm">
              <h3 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                <DocumentTextIcon class="w-5 h-5 text-primary-500" />
                Qo'shimcha ma'lumotlar
              </h3>
              <p class="text-slate-600 leading-relaxed">
                {{ student.notes || "Qo'shimcha izohlar mavjud emas." }}
              </p>
              
              <div class="mt-6 grid grid-cols-2 gap-4 pt-6 border-t border-slate-50">
                <div>
                  <p class="text-xs text-slate-400 mb-1">Ro'yxatdan o'tgan sana</p>
                  <p class="text-sm font-medium text-slate-700">{{ formatDateTime(student.created_at) }}</p>
                </div>
                <div>
                  <p class="text-xs text-slate-400 mb-1">Oxirgi yangilanish</p>
                  <p class="text-sm font-medium text-slate-700">{{ formatDateTime(student.updated_at) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Sidebar Stats/Actions -->
          <div class="space-y-6">
            <div class="bg-white rounded-2xl border border-slate-100 p-6 shadow-sm">
              <h3 class="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4">Statistika</h3>
              <div class="space-y-4">
                <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50">
                  <span class="text-sm text-slate-600">Guruhlar</span>
                  <span class="font-bold text-slate-800">0</span>
                </div>
                <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50">
                  <span class="text-sm text-slate-600">To'lovlar</span>
                  <span class="font-bold text-slate-800">0 UZS</span>
                </div>
                <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50">
                  <span class="text-sm text-slate-600">Davomat</span>
                  <span class="font-bold text-slate-800">0%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-12">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-100 mb-4">
            <UserIcon class="w-8 h-8 text-slate-400" />
          </div>
          <h3 class="text-lg font-medium text-slate-900">Talaba topilmadi</h3>
          <p class="text-slate-500 mt-1">Qidirayotgan talabangiz bazada mavjud emas.</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { 
  ArrowLeftIcon, 
  PencilIcon, 
  UserIcon, 
  PhoneIcon, 
  EnvelopeIcon, 
  DocumentTextIcon 
} from '@heroicons/vue/24/outline'
import Sidebar from '@/components/common/Sidebar.vue'
import Navbar from '@/components/common/Navbar.vue'
import Loading from '@/components/common/Loading.vue'
import { useStudentStore } from '@/store/modules/students'
import { useAuthStore } from '@/store/modules/auth'
import { formatDateTime } from '@/utils/helpers'

const route = useRoute()
const studentStore = useStudentStore()
const authStore = useAuthStore()

const isMentor = computed(() => authStore.userRole === 'MENTOR')

const student = computed(() => {
  const data = studentStore.currentStudent
  if (!data) return {}
  return {
    ...data,
    full_name: `${data.first_name ?? ''} ${data.last_name ?? ''}`.trim(),
  }
})

onMounted(() => {
  const id = route.params.id
  if (id) {
    studentStore.fetchStudentById(id)
  }
})
</script>

import { defineStore } from 'pinia'
import studentService from '@/services/student.service'

export const useStudentStore = defineStore('students', {
  state: () => ({
    students: [],
    currentStudent: null,
    loading: false,
    error: null,
    pagination: {
      count: 0,
      totalPages: 0,
      currentPage: 1,
    },
  }),

  getters: {
    activeStudents: (state) => {
      return state.students.filter(s => s.is_active)
    },
    totalStudents: (state) => state.pagination.count,
  },

  actions: {
    async fetchStudents(params = {}) {
      this.loading = true
      this.error = null
      try {
        const response = await studentService.getAll(params)
        this.students = response.data.results || response.data
        this.pagination = {
          count: response.data.count || this.students.length,
          totalPages: response.data.total_pages || 1,
          currentPage: response.data.current_page || 1,
        }
      } catch (error) {
        this.error = error.response?.data || 'Talabalarni yuklashda xatolik'
      } finally {
        this.loading = false
      }
    },

    async fetchStudentById(id) {
      this.loading = true
      this.error = null
      try {
        const response = await studentService.getById(id)
        this.currentStudent = response.data
      } catch (error) {
        this.error = error.response?.data || "Talaba ma'lumotlarini yuklashda xatolik"
      } finally {
        this.loading = false
      }
    },

    async createStudent(data) {
      this.loading = true
      this.error = null
      try {
        await studentService.create(data)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || 'Talaba yaratishda xatolik'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updateStudent(id, data) {
      this.loading = true
      this.error = null
      try {
        await studentService.update(id, data)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || 'Talaba yangilashda xatolik'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteStudent(id) {
      this.loading = true
      this.error = null
      try {
        await studentService.delete(id)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || "Talaba o'chirishda xatolik"
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async searchStudents(query) {
      this.loading = true
      this.error = null
      try {
        const response = await studentService.search(query)
        this.students = response.data.results || response.data
      } catch (error) {
        this.error = error.response?.data
      } finally {
        this.loading = false
      }
    },
  },
})

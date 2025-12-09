import { defineStore } from 'pinia'
import groupService from '@/services/group.service'
import userService from '@/services/user.service'
import { useAuthStore } from '@/store/modules/auth'

export const useGroupStore = defineStore('groups', {
  state: () => ({
    groups: [],
    currentGroup: null,
    mentors: [],
    loading: false,
    detailLoading: false,
    mentorsLoading: false,
    error: null,
    pagination: {
      count: 0,
      totalPages: 1,
      currentPage: 1,
      pageSize: 10,
    },
    filters: {
      search: '',
      mentor: null,
    },
  }),

  getters: {
    totalGroups: (state) => state.pagination.count,
    activeGroups: (state) => {
      const today = new Date()
      return state.groups.filter((group) => !group.end_date || new Date(group.end_date) >= today)
    },
  },

  actions: {
    async fetchGroups(params = {}) {
      this.loading = true
      this.error = null
      try {
        const authStore = useAuthStore()
        const isMentor = authStore.userRole === 'MENTOR'
        const pageSize = params.page_size || this.pagination.pageSize || 10
        const mentorFilter = isMentor ? null : params.mentor ?? this.filters.mentor
        const response = await groupService.getAll({
          page: params.page ?? this.pagination.currentPage,
          page_size: pageSize,
          search: params.search ?? this.filters.search,
          mentor: mentorFilter || undefined,
          ordering: params.ordering,
        })

        const data = response.data
        this.groups = data.results || data
        const totalCount = data.count ?? this.groups.length
        const totalPages =
          data.total_pages ??
          (totalCount && pageSize ? Math.max(1, Math.ceil(totalCount / pageSize)) : 1)

        this.pagination = {
          count: totalCount,
          totalPages,
          currentPage: data.current_page ?? params.page ?? 1,
          pageSize,
        }

        this.filters = {
          search: params.search ?? this.filters.search,
          mentor: mentorFilter,
        }
      } catch (error) {
        this.error = error.response?.data || "Guruhlarni yuklashda xatolik yuz berdi"
      } finally {
        this.loading = false
      }
    },

    async fetchGroupById(id) {
      this.detailLoading = true
      this.error = null
      try {
        const response = await groupService.getById(id)
        this.currentGroup = response.data
      } catch (error) {
        this.error = error.response?.data || "Guruh ma'lumotlarini yuklashda xatolik"
        throw error
      } finally {
        this.detailLoading = false
      }
    },

    async createGroup(payload) {
      this.loading = true
      this.error = null
      try {
        await groupService.create(payload)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || "Guruh yaratishda xatolik"
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updateGroup(id, payload) {
      this.loading = true
      this.error = null
      try {
        await groupService.update(id, payload)
        if (this.currentGroup?.id === id) {
          await this.fetchGroupById(id)
        }
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || "Guruhni yangilashda xatolik"
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteGroup(id) {
      this.loading = true
      this.error = null
      try {
        await groupService.delete(id)
        this.groups = this.groups.filter((group) => group.id !== id)
        this.pagination.count = Math.max(0, this.pagination.count - 1)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || "Guruhni o'chirishda xatolik"
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async assignMentor(groupId, mentorId) {
      this.loading = true
      try {
        await groupService.assignMentor(groupId, mentorId)
        if (this.currentGroup?.id === groupId) {
          await this.fetchGroupById(groupId)
        } else {
          await this.fetchGroups()
        }
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || 'Mentor tayinlashda xatolik'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchMentors(params = {}) {
      this.mentorsLoading = true
      try {
        const response = await userService.getByRole('mentor', params)
        this.mentors = response.data.results || response.data
      } catch (error) {
        this.error = error.response?.data || 'Mentorlarni yuklashda xatolik'
      } finally {
        this.mentorsLoading = false
      }
    },

    async createEnrollment(payload) {
      this.loading = true
      try {
        await groupService.createEnrollment(payload)
        if (payload.group && this.currentGroup?.id === payload.group) {
          await this.fetchGroupById(payload.group)
        }
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || "Talabani guruhga qo'shishda xatolik"
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updateEnrollment(id, payload) {
      this.loading = true
      try {
        await groupService.updateEnrollment(id, payload)
        if (this.currentGroup?.id) {
          await this.fetchGroupById(this.currentGroup.id)
        }
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || "Talaba ma'lumotini yangilashda xatolik"
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteEnrollment(id) {
      this.loading = true
      try {
        await groupService.deleteEnrollment(id)
        if (this.currentGroup?.id) {
          await this.fetchGroupById(this.currentGroup.id)
        }
        return { success: true }
      } catch (error) {
        this.error = error.response?.data || "Talabani guruhdan o'chirishda xatolik"
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchEnrollments(params = {}) {
      try {
        const response = await groupService.getEnrollments(params)
        return response.data.results || response.data
      } catch (error) {
        this.error = error.response?.data || "Enrollments ma'lumotlarini yuklashda xatolik"
        throw error
      }
    },
  },
})

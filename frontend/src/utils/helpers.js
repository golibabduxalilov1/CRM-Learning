import dayjs from 'dayjs'
import 'dayjs/locale/uz-latn'

dayjs.locale('uz-latn')

export const formatMoney = (amount) => {
  if (!amount && amount !== 0) return '0 so\'m'
  return new Intl.NumberFormat('uz-UZ', {
    style: 'decimal',
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(amount) + ' so\'m'
}

export const formatDate = (date, format = 'DD.MM.YYYY') => {
  if (!date) return '-'
  return dayjs(date).format(format)
}

export const formatDateTime = (date, format = 'DD.MM.YYYY HH:mm') => {
  if (!date) return '-'
  return dayjs(date).format(format)
}

export const formatRelativeTime = (date) => {
  if (!date) return '-'
  return dayjs(date).fromNow()
}

export const getStatusBadge = (status) => {
  const badges = {
    PENDING: { text: 'Kutilmoqda', class: 'badge-warning' },
    PAID: { text: 'To\'langan', class: 'badge-success' },
    OVERDUE: { text: 'Muddati o\'tgan', class: 'badge-danger' },
    CANCELLED: { text: 'Bekor qilingan', class: 'bg-gray-100 text-gray-800' },
    ACTIVE: { text: 'Faol', class: 'badge-success' },
    PAUSED: { text: 'To\'xtatilgan', class: 'badge-warning' },
    COMPLETED: { text: 'Tugatilgan', class: 'badge-primary' },
    DROPPED: { text: 'Tashlab ketgan', class: 'badge-danger' },
    CALCULATED: { text: 'Hisoblangan', class: 'badge-warning' },
  }
  return badges[status] || { text: status, class: 'bg-gray-100 text-gray-800' }
}

export const debounce = (func, wait = 300) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

export const truncate = (str, length = 50) => {
  if (!str) return ''
  return str.length > length ? str.substring(0, length) + '...' : str
}

export const getRoleLabel = (role) => {
  const labels = {
    SUPERADMIN: 'Superadmin',
    BOSS: 'Boss',
    ADMIN: 'Administrator',
    MENTOR: 'Mentor',
  }
  return labels[role] || role
}

export const downloadFile = (data, filename, type = 'text/csv') => {
  const blob = new Blob([data], { type })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = filename
  link.click()
  URL.revokeObjectURL(link.href)
}

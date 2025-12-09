export const USER_ROLES = {
  SUPERADMIN: 'SUPERADMIN',
  BOSS: 'BOSS',
  ADMIN: 'ADMIN',
  MENTOR: 'MENTOR',
}

export const PAYMENT_STATUS = {
  PENDING: 'PENDING',
  PAID: 'PAID',
  OVERDUE: 'OVERDUE',
  CANCELLED: 'CANCELLED',
}

export const ENROLLMENT_STATUS = {
  ACTIVE: 'ACTIVE',
  PAUSED: 'PAUSED',
  COMPLETED: 'COMPLETED',
  DROPPED: 'DROPPED',
}

export const PAYOUT_STATUS = {
  CALCULATED: 'CALCULATED',
  PAID: 'PAID',
  CANCELLED: 'CANCELLED',
}

export const ROUTES = {
  WELCOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  STUDENTS: '/students',
  GROUPS: '/groups',
  PAYMENTS: '/payments',
  PAYOUTS: '/payouts',
  SETTINGS_COMMISSION: '/settings/commission',
  SETTINGS_ALLOWLIST: '/settings/allowlist',
  SETTINGS_PROFILE: '/settings/profile',
}

export const API_ENDPOINTS = {
  AUTH: {
    REGISTER: '/auth/register/',
    LOGIN: '/auth/login/',
    VERIFY_OTP: '/auth/otp/verify/',
    LOGOUT: '/auth/logout/',
    ME: '/auth/me/',
  },
  STUDENTS: '/students/',
  GROUPS: '/groups/',
  PAYMENTS: '/payments/',
  PAYOUTS: '/payouts/mentor/',
  ANALYTICS: '/dashboard/',
}

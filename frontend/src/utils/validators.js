export const required = (value) => {
  if (Array.isArray(value)) {
    return value.length > 0 || 'Bu maydon majburiy'
  }
  return !!value || 'Bu maydon majburiy'
}

export const email = (value) => {
  if (!value) return true
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return pattern.test(value) || 'Email noto\'g\'ri formatda'
}

export const minLength = (min) => (value) => {
  if (!value) return true
  return value.length >= min || `Kamida ${min} ta belgi bo'lishi kerak`
}

export const maxLength = (max) => (value) => {
  if (!value) return true
  return value.length <= max || `Ko'pi bilan ${max} ta belgi bo'lishi kerak`
}

export const phone = (value) => {
  if (!value) return true
  const pattern = /^\+?998[0-9]{9}$/
  return pattern.test(value.replace(/\s/g, '')) || 'Telefon raqami noto\'g\'ri formatda (+998901234567)'
}

export const numeric = (value) => {
  if (value === '' || value === null || value === undefined) return true
  return !isNaN(value) || 'Faqat raqam kiritish mumkin'
}

export const positiveNumber = (value) => {
  if (value === '' || value === null || value === undefined) return true
  return (Number(value) >= 0) || 'Faqat musbat raqam kiritish mumkin'
}

export const percentage = (value) => {
  if (value === '' || value === null || value === undefined) return true
  const num = Number(value)
  return (num >= 0 && num <= 100) || 'Foiz 0 dan 100 gacha bo\'lishi kerak'
}

export const dateAfter = (compareDate) => (value) => {
  if (!value || !compareDate) return true
  return new Date(value) > new Date(compareDate) || 'Sana keyinroq bo\'lishi kerak'
}

export const dateBefore = (compareDate) => (value) => {
  if (!value || !compareDate) return true
  return new Date(value) < new Date(compareDate) || 'Sana oldinroq bo\'lishi kerak'
}

export const passwordStrength = (value) => {
  if (!value) return true
  const hasUpperCase = /[A-Z]/.test(value)
  const hasLowerCase = /[a-z]/.test(value)
  const hasNumbers = /\d/.test(value)
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(value)
  
  if (value.length < 8) return 'Parol kamida 8 ta belgidan iborat bo\'lishi kerak'
  if (!hasUpperCase) return 'Parol kamida bitta katta harf bo\'lishi kerak'
  if (!hasLowerCase) return 'Parol kamida bitta kichik harf bo\'lishi kerak'
  if (!hasNumbers) return 'Parol kamida bitta raqam bo\'lishi kerak'
  
  return true
}

export const matchPassword = (password) => (value) => {
  return value === password || 'Parollar mos kelmaydi'
}

/** Small pure helpers (validation, formatting). */

export const isEmail = (email: string) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.trim())

export const isPhone = (phone: string) => /^\+?[0-9]{8,15}$/.test(phone.replace(/\s/g, ''))

/** Same rules as the backend (User.validate_password). */
export const isPassword = (password: string) =>
  password.length >= 8 &&
  /\d/.test(password) &&
  /[a-z]/.test(password) &&
  /[A-Z]/.test(password) &&
  /[!@#$%^&*()_+\-=.,;:?]/.test(password)

export const isName = (name: string) => /^[\p{L}\s.'-]+$/u.test(name.trim())

export const getCurrentYear = () => new Date().getFullYear()

/** YYYY-MM-DD in local time */
export function getCurrentDate() {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

export const removeSpecialCharacters = (str: string) => str.replace(/[^a-zA-Z0-9]/g, '')

export const capitalizeFirstCharacter = (str: string) => (str ? str.charAt(0).toUpperCase() + str.slice(1) : '')

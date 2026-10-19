/** Same rules as the FastAPI backend (User.validate_password). Return an error message or null. */

export const validateEmail = (v: string) => (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? null : 'Email invalide');

export const validateRequired = (v: string, label: string) => (v.trim() ? null : `${label} requis`);

export function validatePassword(v: string): string | null {
  if (v.length < 8) return '8 caractères minimum';
  if (!/[A-Z]/.test(v)) return 'Une majuscule requise';
  if (!/[a-z]/.test(v)) return 'Une minuscule requise';
  if (!/\d/.test(v)) return 'Un chiffre requis';
  if (!/[!@#$%^&*()_+\-=.,;:?]/.test(v)) return 'Un caractère spécial requis';
  return null;
}

export const validatePhone = (v: string) =>
  !v.trim() || /^\+?[0-9]{8,15}$/.test(v.replace(/\s/g, '')) ? null : 'Numéro invalide';

import { toast } from 'react-toastify'
import { ApiError, Get, Send } from '@/services/service.api'
import type { LoginPayload } from '@/hooks/hooks.authSlice'
import type { LoginResponse, User } from '@/types/types'
import { isEmail, isName, isPassword } from './controller.utils'

function toastError(error: unknown, fallback: string) {
  toast.error(error instanceof ApiError ? error.message : fallback)
}

/** Returns the payload for the `login` action, or null when it failed (a toast is shown). */
export async function handleLogin(email: string, password: string, remember: boolean): Promise<LoginPayload | null> {
  if (!email || !password) {
    toast.error('Please fill in every field')
    return null
  }
  try {
    const { access_token, token_type: _t, expires_in, ...user } = await Send<LoginResponse>('/user/login', { email, password })
    toast.success('Logged in')
    return { user, token: access_token, expiresIn: expires_in, remember }
  } catch (error) {
    toastError(error, 'Login failed')
    return null
  }
}

export interface SignupForm {
  nom: string
  prenom: string
  email: string
  password: string
  tel?: string
}

export async function handleSignup(form: SignupForm): Promise<boolean> {
  if (!isName(form.nom) || !isName(form.prenom)) return (toast.error('Invalid name'), false)
  if (!isEmail(form.email)) return (toast.error('Invalid email'), false)
  if (!isPassword(form.password)) {
    toast.error('Password: 8+ chars with upper, lower, digit and special character')
    return false
  }
  try {
    await Send('/user/signin', form)
    toast.success('Account created, you can log in')
    return true
  } catch (error) {
    toastError(error, 'Sign up failed')
    return false
  }
}

export async function fetchMe(): Promise<User | null> {
  try {
    return (await Get<{ user: User }>('/user/me')).user
  } catch {
    return null
  }
}

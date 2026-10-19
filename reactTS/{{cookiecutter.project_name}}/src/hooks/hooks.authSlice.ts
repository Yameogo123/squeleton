import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import type { User } from '@/types/types'

export interface AuthState {
  user: User | null
  token: string
  expiresAt: number | null // epoch ms
  remember: boolean
  loading: boolean
}

export const initialAuthState: AuthState = { user: null, token: '', expiresAt: null, remember: false, loading: false }

export interface LoginPayload {
  user: User
  token: string
  expiresIn: number // seconds
  remember: boolean
}

const authSlice = createSlice({
  name: 'auth',
  initialState: initialAuthState,
  reducers: {
    login(state, action: PayloadAction<LoginPayload>) {
      const { user, token, expiresIn, remember } = action.payload
      state.user = user
      state.token = token
      state.expiresAt = Date.now() + expiresIn * 1000
      state.remember = remember
    },
    logout() {
      return initialAuthState
    },
    setLoading(state, action: PayloadAction<boolean>) {
      state.loading = action.payload
    },
    userUpdate(state, action: PayloadAction<Partial<User>>) {
      if (state.user) state.user = { ...state.user, ...action.payload }
    },
  },
})

export const { login, logout, setLoading, userUpdate } = authSlice.actions
export default authSlice.reducer

import type { AuthState } from './hooks.authSlice'

const KEY = '{{ cookiecutter.project_slug }}_auth'

/**
 * Auth persistence.
 * - "remember me" -> localStorage, otherwise sessionStorage (cleared when the tab closes)
 * - only our own key is touched (never localStorage.clear())
 * - expired / malformed data is dropped on load
 *
 * Note: any JS running on the page can read web storage. Keep a strict CSP (see
 * security-headers.ts) and, for higher security, move the token to an httpOnly cookie.
 */
export function loadAuth(): AuthState | undefined {
  for (const storage of [sessionStorage, localStorage]) {
    try {
      const raw = storage.getItem(KEY)
      if (!raw) continue
      const state = JSON.parse(raw) as AuthState
      if (typeof state?.token !== 'string' || !state.expiresAt || state.expiresAt <= Date.now()) {
        storage.removeItem(KEY)
        continue
      }
      return { ...state, loading: false }
    } catch {
      storage.removeItem(KEY)
    }
  }
  return undefined
}

export function saveAuth(state: AuthState) {
  try {
    clearAuth()
    if (!state.token) return
    const storage = state.remember ? localStorage : sessionStorage
    storage.setItem(KEY, JSON.stringify({ ...state, loading: false }))
  } catch {
    // storage full / disabled (private mode): stay logged in for this page only
  }
}

export function clearAuth() {
  sessionStorage.removeItem(KEY)
  localStorage.removeItem(KEY)
}

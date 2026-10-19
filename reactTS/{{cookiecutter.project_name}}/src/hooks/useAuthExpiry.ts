import { useEffect } from 'react'
import { logout } from './hooks.authSlice'
import { useAppDispatch, useAppSelector } from './hooks.store'

/** Logs the user out exactly when the token expires. */
export function useAuthExpiry() {
  const expiresAt = useAppSelector((s) => s.auth.expiresAt)
  const dispatch = useAppDispatch()

  useEffect(() => {
    if (!expiresAt) return
    const delay = expiresAt - Date.now()
    if (delay <= 0) {
      dispatch(logout())
      return
    }
    // setTimeout overflows above ~24.8 days
    const timer = setTimeout(() => dispatch(logout()), Math.min(delay, 2 ** 31 - 1))
    return () => clearTimeout(timer)
  }, [expiresAt, dispatch])
}

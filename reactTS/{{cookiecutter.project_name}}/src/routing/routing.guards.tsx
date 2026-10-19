import { Navigate, Outlet, useLocation } from 'react-router'
import { useAppSelector } from '@/hooks/hooks.store'

const useIsAuthenticated = () => useAppSelector((s) => Boolean(s.auth.token && s.auth.user))

/** Only for logged-in users: otherwise redirect to /login and come back after. */
export function ProtectedRoute() {
  const location = useLocation()
  const authenticated = useIsAuthenticated()
  const state = { from: location.pathname }
  if (!authenticated) return <Navigate to="/login" replace state={state} />
  return <Outlet />
}

/** Only for anonymous users (login / sign-in pages). */
export function PublicOnlyRoute() {
  const authenticated = useIsAuthenticated()
  if (authenticated) return <Navigate to="/" replace />
  return <Outlet />
}

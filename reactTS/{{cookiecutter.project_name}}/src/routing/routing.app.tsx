import { lazy, Suspense } from 'react'
import { Route, Routes } from 'react-router'
import ViewLayout from '@/views/template/view.layout'
import { ProtectedRoute, PublicOnlyRoute } from './routing.guards'

// code-splitting: each page is its own chunk
const Home = lazy(() => import('@/views/view.home'))
const Login = lazy(() => import('@/views/security/login'))
const Signin = lazy(() => import('@/views/security/signin'))
const NotFound = lazy(() => import('@/views/view.notFound'))

export default function AppRouting() {
  return (
    <Suspense fallback={<div className="p-6 text-slate-500">Chargement…</div>}>
      <Routes>
        <Route element={<PublicOnlyRoute />}>
          <Route path="/login" element={<Login />} />
          <Route path="/signin" element={<Signin />} />
        </Route>
        <Route element={<ProtectedRoute />}>
          <Route element={<ViewLayout />}>
            <Route path="/" element={<Home />} />
          </Route>
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Suspense>
  )
}

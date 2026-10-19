import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import { useAuthExpiry } from '@/hooks/useAuthExpiry'
import AppRouting from '@/routing/routing.app'

export default function App() {
  useAuthExpiry()

  return (
    <>
      <AppRouting />
      <ToastContainer position="top-right" newestOnTop />
    </>
  )
}

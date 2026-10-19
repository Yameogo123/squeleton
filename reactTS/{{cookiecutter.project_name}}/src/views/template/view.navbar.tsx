import { LogOut } from 'lucide-react'
import { logout } from '@/hooks/hooks.authSlice'
import { useAppDispatch, useAppSelector } from '@/hooks/hooks.store'

export default function ViewNavbar() {
  const user = useAppSelector((s) => s.auth.user)
  const dispatch = useAppDispatch()

  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-3">
      <span className="font-semibold">{{ cookiecutter.site_title }}</span>
      <div className="flex items-center gap-4 text-sm">
        <span>{user?.prenom} {user?.nom}</span>
        <button type="button" onClick={() => dispatch(logout())} className="flex items-center gap-1 text-slate-600 hover:text-slate-900">
          <LogOut size={16} /> Déconnexion
        </button>
      </div>
    </header>
  )
}

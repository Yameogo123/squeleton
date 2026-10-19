import { Home } from 'lucide-react'
import { NavLink } from 'react-router'

const link = ({ isActive }: { isActive: boolean }) =>
  `flex items-center gap-2 rounded-lg px-3 py-2 ${isActive ? 'bg-slate-900 text-white' : 'text-slate-700 hover:bg-slate-100'}`

export default function ViewSidebar() {
  return (
    <nav className="hidden w-56 shrink-0 border-r border-slate-200 bg-white p-3 md:block">
      <NavLink to="/" end className={link}>
        <Home size={16} /> Accueil
      </NavLink>
    </nav>
  )
}

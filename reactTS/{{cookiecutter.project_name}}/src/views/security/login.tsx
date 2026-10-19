import { useState, type FormEvent } from 'react'
import { Link, useLocation, useNavigate } from 'react-router'
import { handleLogin } from '@/controllers/controller.user'
import { login } from '@/hooks/hooks.authSlice'
import { useAppDispatch } from '@/hooks/hooks.store'

const input = 'w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200'

export default function Login() {
  const [email, setEmail] = useState('')
  const [pwd, setPwd] = useState('')
  const [remember, setRemember] = useState(false)
  const [disabled, setDisabled] = useState(false)
  const dispatch = useAppDispatch()
  const navigate = useNavigate()
  const location = useLocation()
  // go back to the page that required auth (only internal paths: no open redirect)
  const from = (location.state as { from?: string } | null)?.from
  const redirectTo = from?.startsWith('/') && !from.startsWith('//') ? from : '/'

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setDisabled(true)
    const payload = await handleLogin(email, pwd, remember)
    setDisabled(false)
    if (payload) {
      dispatch(login(payload))
      navigate(redirectTo, { replace: true })
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 p-4">
      <form onSubmit={onSubmit} className="w-full max-w-sm space-y-4 rounded-2xl bg-white p-8 shadow">
        <h1 className="text-2xl font-semibold">Se connecter</h1>
        <label className="block">
          <span className="sr-only">Email</span>
          <input type="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} className={input} placeholder="email" />
        </label>
        <label className="block">
          <span className="sr-only">Mot de passe</span>
          <input type="password" autoComplete="current-password" required value={pwd} onChange={(e) => setPwd(e.target.value)} className={input} placeholder="mot de passe" />
        </label>
        <label className="flex items-center gap-2 text-sm text-slate-600">
          <input type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)} />
          Rester connecté
        </label>
        <button type="submit" disabled={disabled} className="w-full rounded-lg bg-slate-900 py-3 font-medium text-white disabled:opacity-50">
          {disabled ? 'Connexion…' : 'CONNEXION'}
        </button>
        <p className="text-center text-sm text-slate-600">
          Pas de compte ? <Link to="/signin" className="font-medium text-slate-900 underline">Créer</Link>
        </p>
      </form>
    </main>
  )
}

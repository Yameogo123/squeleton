import { useState, type ChangeEvent, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router'
import { handleSignup, type SignupForm } from '@/controllers/controller.user'

const input = 'w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-slate-900 focus:ring-2 focus:ring-slate-200'

export default function Signin() {
  const [form, setForm] = useState<SignupForm>({ nom: '', prenom: '', email: '', password: '', tel: '' })
  const [disabled, setDisabled] = useState(false)
  const navigate = useNavigate()

  const set = (field: keyof SignupForm) => (e: ChangeEvent<HTMLInputElement>) => setForm({ ...form, [field]: e.target.value })

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setDisabled(true)
    const ok = await handleSignup(form)
    setDisabled(false)
    if (ok) navigate('/login')
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 p-4">
      <form onSubmit={onSubmit} className="w-full max-w-sm space-y-4 rounded-2xl bg-white p-8 shadow">
        <h1 className="text-2xl font-semibold">Créer un compte</h1>
        <input required value={form.nom} onChange={set('nom')} className={input} placeholder="nom" aria-label="nom" />
        <input required value={form.prenom} onChange={set('prenom')} className={input} placeholder="prénom" aria-label="prénom" />
        <input required type="email" autoComplete="email" value={form.email} onChange={set('email')} className={input} placeholder="email" aria-label="email" />
        <input type="tel" autoComplete="tel" value={form.tel} onChange={set('tel')} className={input} placeholder="téléphone (optionnel)" aria-label="téléphone" />
        <input required type="password" autoComplete="new-password" minLength={8} value={form.password} onChange={set('password')} className={input} placeholder="mot de passe" aria-label="mot de passe" />
        <button type="submit" disabled={disabled} className="w-full rounded-lg bg-slate-900 py-3 font-medium text-white disabled:opacity-50">
          CRÉER
        </button>
        <p className="text-center text-sm text-slate-600">
          Déjà inscrit ? <Link to="/login" className="font-medium text-slate-900 underline">Se connecter</Link>
        </p>
      </form>
    </main>
  )
}

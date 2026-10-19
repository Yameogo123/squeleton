import { useAppSelector } from '@/hooks/hooks.store'

export default function Home() {
  const user = useAppSelector((s) => s.auth.user)

  return (
    <section className="space-y-2">
      <h1 className="text-2xl font-semibold">Bonjour {user?.prenom} 👋</h1>
      <p className="text-slate-600">Start building your pages in src/views.</p>
    </section>
  )
}

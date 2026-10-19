import { Link } from 'react-router'

export default function NotFound() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-4xl font-bold">404</h1>
      <Link to="/" className="underline">Retour à l'accueil</Link>
    </main>
  )
}

import { getCurrentYear } from '@/controllers/controller.utils'

export default function ViewFooter() {
  return <footer className="border-t border-slate-200 px-6 py-3 text-center text-xs text-slate-500">© {getCurrentYear()} {{ cookiecutter.author_name }}</footer>
}

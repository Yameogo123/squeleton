import { Outlet } from 'react-router'
import ViewFooter from './view.footer'
import ViewNavbar from './view.navbar'
import ViewSidebar from './view.sidebar'

export default function ViewLayout() {
  return (
    <div className="flex min-h-screen flex-col bg-slate-50">
      <ViewNavbar />
      <div className="flex flex-1">
        <ViewSidebar />
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
      <ViewFooter />
    </div>
  )
}

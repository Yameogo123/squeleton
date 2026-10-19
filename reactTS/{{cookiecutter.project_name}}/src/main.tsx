import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import App from './App'
import './css/index.css'
import { logout } from './hooks/hooks.authSlice'
import Provide from './hooks/hooks.provider'
import { store } from './hooks/hooks.store'
import { configureApi } from './services/service.api'
import ErrorBoundary from './views/view.errorBoundary'

configureApi({
  getToken: () => store.getState().auth.token || null,
  onUnauthorized: () => store.dispatch(logout()),
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary>
      <Provide>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Provide>
    </ErrorBoundary>
  </StrictMode>,
)

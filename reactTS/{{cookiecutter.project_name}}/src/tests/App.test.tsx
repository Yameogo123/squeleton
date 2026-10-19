import { render, screen } from '@testing-library/react'
import { Provider } from 'react-redux'
import { MemoryRouter } from 'react-router'
import App from '@/App'
import { makeStore } from '@/hooks/hooks.store'

function renderAt(path: string, store = makeStore()) {
  return render(
    <Provider store={store}>
      <MemoryRouter initialEntries={[path]}>
        <App />
      </MemoryRouter>
    </Provider>,
  )
}

test('anonymous user is redirected to the login page', async () => {
  renderAt('/')
  expect(await screen.findByRole('heading', { name: /se connecter/i })).toBeInTheDocument()
})

test('authenticated user sees the home page', async () => {
  const store = makeStore({
    user: { _id: '1', nom: 'Doe', prenom: 'Jo', email: 'jo@x.com', role: 'user' },
    token: 'token',
    expiresAt: Date.now() + 60_000,
    remember: false,
    loading: false,
  })
  renderAt('/', store)
  expect(await screen.findByRole('heading', { name: /bonjour jo/i })).toBeInTheDocument()
})

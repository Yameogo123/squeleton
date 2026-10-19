# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

React 19 + TypeScript (strict) + Vite, Redux Toolkit, React Router, Tailwind CSS 4, Vitest, oxlint.

## Quick start

```bash
make use-node    # optional: Node version from .nvmrc (nvm)
make install
make dev         # http://localhost:5173
make check       # lint + typecheck + tests
```

The API URL comes from `VITE_API_URL` (`.env.local`, created at generation from `.env.example`).
Everything prefixed `VITE_` is **public** (bundled in the JS): never put a secret there.

Commit `package-lock.json`: it pins the exact dependency tree (`npm ci` in CI / Docker).

## Architecture

```
├── index.html                 <- entry HTML
├── vite.config.ts             <- build, dev server, tests config
├── security-headers.ts        <- CSP + security headers (dev / preview)
├── public/                    <- static files (+ _headers / _redirects for Netlify/Cloudflare)
├── firebase.json, nginx.conf, Dockerfile   <- hosting with the same security headers
└── src
    ├── main.tsx               <- providers, router, API wiring
    ├── App.tsx                <- routes + toasts + token expiry
    ├── controllers/           <- (2) business logic calling the services (validation, toasts)
    ├── services/              <- (1) typed API client (fetch, token, timeout, errors)
    ├── hooks/                 <- Redux store, auth slice, persistence, custom hooks
    ├── routing/               <- routes, ProtectedRoute / PublicOnlyRoute guards
    ├── views/                 <- pages (security/, template/ layout, home, 404, error boundary)
    ├── types/                 <- shared TypeScript types (API models)
    ├── css/                   <- Tailwind entry
    └── tests/                 <- Vitest + Testing Library
```

## Security notes

- Strict CSP (`script-src 'self'`): no inline scripts, no third-party scripts unless you add them to
  `security-headers.ts` **and** `public/_headers` / `firebase.json` / `nginx.conf`.
- Test the real CSP with `make preview` (the dev server can't use it because of HMR).
- Token: kept in Redux, persisted in `sessionStorage` (or `localStorage` with "Rester connecté"),
  auto-logout on expiry and on any 401. For stronger protection against XSS, move to an httpOnly cookie.
- No secrets / third-party API keys in the front end: call those services through your backend.
- `npm run audit` for known vulnerabilities; `.npmrc` refuses peer-dependency conflicts.

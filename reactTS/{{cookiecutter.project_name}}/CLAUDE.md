# {{ cookiecutter.project_name }} — React + TypeScript front end

{{ cookiecutter.description }}

React 19 · TypeScript strict · Vite · React Router · Redux Toolkit · Tailwind 4 · Vitest · oxlint.
Layout: see `ARCHITECTURE.md` (read it when you need to locate code).

## Commands

```bash
npm install
npm run dev            # http://localhost:5173
make check             # lint + typecheck + tests (definition of done)
npx vitest run src/tests/x.test.ts   # single test file
npm run build && npm run preview     # production build with the real CSP
npm run audit
```

**Definition of done**: `make check` green (and `npm run build` if config/deps changed).

## Conventions

- Data flow: view → controller (validation, toasts) → service (`service.api.ts` typed fetch). Views never call `fetch`.
- Types for every API payload in `src/types/`; no `any` (use `unknown` + narrowing).
- State: server data in components/hooks, global session only in the Redux `auth` slice; typed hooks
  `useAppDispatch` / `useAppSelector`.
- Routes in `routing/routing.app.tsx`, lazy-loaded; protected pages under `ProtectedRoute`.
- Styling: Tailwind utilities, no inline style objects; reuse existing components before creating new ones.
- Tests next to the feature in `src/tests/` (Testing Library: query by role/label, not class names).

## Security rules

- No `dangerouslySetInnerHTML`, no `eval`, no `target="_blank"` without `rel="noopener noreferrer"`.
- Everything `VITE_*` is public: never put secrets/API keys in the front end — call them through the backend.
- New external origin (API, CDN, fonts, analytics) → update the CSP in `security-headers.ts` AND
  `public/_headers`, `firebase.json`, `nginx.conf`.
- Redirects only to internal paths (no open redirect); token handling only in `hooks.storage.ts` / auth slice.

## Secrets (hard rules, enforced by `.claude/hooks/`)

- Never read, print, copy, grep or edit `.env*` files (except `.env.example` / `.env.template`), keys or
  credentials. Variable names live in the template file; values are set by the user.
- Never hard-code a secret, token, password or private URL in code, tests, logs or commit messages.
- New config value → add it to the template file (with a placeholder) and to the typed config.

## Working efficiently (token economy)

- Read only what the task needs: `Grep`/`Glob` first, then targeted `Read` (with offset/limit for big files).
- Never read generated or vendored content: dependencies, lockfiles, build output, caches, data dumps
  (most are denied in `.claude/settings.json`).
- Use `ARCHITECTURE.md` to locate code instead of exploring the tree; read it only when you need it.
- After a small change run the narrowest check (one test file, the lint hook already runs on edited files);
  run the full sanity check once, before saying "done".
- Don't paste whole files or long logs back to the user: summarize and point to `file:line`.
- Use subagents (`code-reviewer`, `security-auditor`, Explore) for broad reviews/searches so their file
  reads stay out of the main context.
- Keep answers short: what changed, how it was verified, what's left.

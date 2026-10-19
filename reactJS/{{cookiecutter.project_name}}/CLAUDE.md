# {{ cookiecutter.project_name }} — React (JavaScript, Create React App)

{{ cookiecutter.description }}

> Legacy template: Create React App is deprecated. For new projects use the `reactTS` template (Vite + TS).

Layout: see `ARCHITECTURE.md`.

## Commands

```bash
npm install
npm start                          # http://localhost:3000
CI=true npm test -- --watchAll=false
npx eslint src
npm run build
```

**Definition of done**: `npx eslint src` clean and `CI=true npm test -- --watchAll=false` green.

## Conventions

- Data flow: view → controller (`src/controllers`) → service (`src/services/service.api.js`). Views never call `fetch`.
- Global state in Redux (`src/hooks`), routes in `src/routing`.
- JSDoc on exported functions (types for editors).

## Security rules

- No `dangerouslySetInnerHTML`/`eval`; no secrets or third-party API keys in the front end (`REACT_APP_*` is public).
- Don't call third-party APIs that need a key from the browser (e.g. SMS gateways): go through the backend.
- Don't `localStorage.clear()`; only remove the app's own keys.

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

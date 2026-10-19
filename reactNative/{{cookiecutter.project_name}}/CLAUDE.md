# {{ cookiecutter.project_name }} — React Native (Expo)

{{ cookiecutter.description }}

Expo SDK 58 · React Native 0.88 · TypeScript strict · Expo Router · expo-secure-store · jest-expo.
Layout: see `ARCHITECTURE.md` (read it when you need to locate code).

## Expo moves fast — don't trust memory

Before using an Expo / React Native API, check the docs of the installed SDK
(`https://docs.expo.dev/versions/v58.0.0/`, index: `https://docs.expo.dev/llms.txt`).

## Commands

```bash
npm install
npx expo start             # dev server (i = iOS, a = Android, w = web)
npm run check              # lint + typecheck + tests (definition of done)
npx jest src/__tests__/x.test.ts   # single test file
npx expo install <pkg>     # ALWAYS instead of npm install <pkg> (SDK-compatible versions)
npx expo-doctor            # dependency / config diagnosis
```

**Definition of done**: `npm run check` green (+ `npx expo-doctor` if dependencies changed).

## Conventions

- `src/app/` = routes only (Expo Router). Logic in `services/`, `context/`, `hooks/`, `lib/`; UI in `components/`.
- Auth is declarative: `Stack.Protected guard` in `src/app/_layout.tsx`; no manual redirects.
- UI: build with `components/ui/*` (Text, Button, TextField, Card, ListItem, Avatar, Screen, EmptyState).
  Colors/spacing/typography only from `constants/theme.ts` via `useTheme()` — no raw hex or magic numbers.
  New color pair → check WCAG AA contrast (4.5:1) in light AND dark before adding the token.
- Every screen handles loading / empty / error / offline; forms validate inline (`lib/validation.ts`).
- Strings are French by default (UI copy); keep them short and action-oriented.
- `ios/` and `android/` are generated (CNG): never edit them, configure via `app.json` / config plugins.
- Tests: jest-expo + Testing Library (query by role/text); native modules mocked in `jest.setup.tsx`.

## Security rules

- Tokens only via `lib/storage.ts` (SecureStore, this-device-only); never AsyncStorage for secrets.
- `EXPO_PUBLIC_*` is bundled in the app = public: no secrets, no private API keys in the app.
- API calls only through `services/api.ts` (timeout, bearer, 401 → logout); HTTPS in production.
- Signing keys, `google-services.json`, `GoogleService-Info.plist` stay out of git (EAS credentials).
- Deep links: validate params before using them; no navigation to arbitrary URLs from params.

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

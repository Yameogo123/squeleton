# Architecture — {{ cookiecutter.project_name }}

## Navigation

```
src/app/_layout.tsx          SafeArea + Session providers, theme, Stack with guards:
  ├─ guard: logged out ──►  login.tsx  ─►  signup.tsx
  └─ guard: logged in  ──►  (tabs)/_layout.tsx   bottom tabs
                              ├─ index.tsx      Accueil
                              ├─ messages.tsx   Messages
                              └─ settings.tsx   Réglages (logout)
src/app/+not-found.tsx       unknown routes
```

## Code

```
src/components/ui/           design system: Text, Button, TextField, Card, ListItem, Avatar, Screen, EmptyState
src/components/              app components (OfflineBanner)
src/constants/theme.ts       tokens: Colors (light/dark), Spacing, Radius, Typography, HitSize
src/context/session.tsx      session (SecureStore), signIn/signOut, expiry timer, 401 → logout
src/services/api.ts          typed fetch (base URL resolution, timeout, ApiError)
src/services/auth.ts         /user/login, /user/signin, /user/me
src/services/messages.ts     placeholder data source for the Messages tab
src/hooks/                   useTheme, useOnline
src/lib/                     storage (SecureStore), validation, dialog (cross-platform confirm)
src/__tests__/               jest-expo tests;  jest.setup.tsx = native mocks
```

## Adding a screen

- Tab: `src/app/(tabs)/<name>.tsx` + `<Tabs.Screen>` in `(tabs)/_layout.tsx` (icon name with `-outline` variant).
- Stack screen pushed from a tab: `src/app/<name>.tsx` (or a group) and `router.push('/<name>')`.
- Wrap content in `<Screen>`, use ui components + tokens, add a test in `src/__tests__/`.

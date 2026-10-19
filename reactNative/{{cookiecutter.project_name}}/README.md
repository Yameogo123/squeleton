# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

Expo SDK 58 · React Native · TypeScript (strict) · Expo Router · Secure Store auth.

## Quick start

```bash
make install
make start          # scan the QR code (Expo Go) or press i / a
make check          # lint + typecheck + tests
```

The API is the FastAPI template (`/user/login`, `/user/signin`, `/user/me`).
In development the API host is the machine running Metro, port {{ cookiecutter.api_port }}: start the API with
`--host 0.0.0.0` so a real phone can reach it. Otherwise set `EXPO_PUBLIC_API_URL` (see `.env.example`).

Add packages with `npx expo install <pkg>` (never plain `npm install`): it picks SDK-compatible versions.

## Screens

| Route | File | |
|---|---|---|
| `/login` | `src/app/login.tsx` | anonymous only |
| `/signup` | `src/app/signup.tsx` | anonymous only |
| `/` | `src/app/(tabs)/index.tsx` | Home tab |
| `/messages` | `src/app/(tabs)/messages.tsx` | Messages tab |
| `/settings` | `src/app/(tabs)/settings.tsx` | Settings tab (logout) |

Access control is declarative in `src/app/_layout.tsx` (`Stack.Protected guard={...}`).

## Architecture

```
src/
├── app/                 <- routes only (Expo Router): login, signup, (tabs) group, _layout (guards)
├── components/ui/       <- design system: Text, Button, TextField, Card, ListItem, Avatar, Screen, EmptyState
├── components/          <- app components (OfflineBanner)
├── constants/theme.ts   <- design tokens: colors (light/dark), spacing, radius, typography
├── context/session.tsx  <- auth session (secure store, expiry, 401 -> logout)
├── hooks/               <- useTheme, useOnline
├── lib/                 <- storage (SecureStore), validation
├── services/            <- api client + endpoints (auth, messages)
└── __tests__/           <- jest-expo + Testing Library
```

## Security

- Token in the iOS Keychain / Android Keystore (`expo-secure-store`, this-device-only), never AsyncStorage.
- `EXPO_PUBLIC_*` values are bundled in the app: no secrets in the app, ever.
- Auto logout at token expiry and on any 401. `android.allowBackup=false`.
- Signing keys / `google-services.json` are gitignored: use EAS credentials.

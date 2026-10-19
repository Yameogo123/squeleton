# Architecture — {{ cookiecutter.project_name }}

```
src/main.tsx                    providers (Redux, Router, ErrorBoundary) + API wiring (token getter, 401 → logout)
src/App.tsx                     routes + toasts + token expiry
src/routing/routing.app.tsx     route table (lazy pages)
src/routing/routing.guards.tsx  ProtectedRoute / PublicOnlyRoute
src/services/service.api.ts     typed fetch: base URL, bearer token, timeout, ApiError
src/controllers/                business logic called by views (validation, toasts)
src/hooks/                      store, auth slice, storage (session/local), custom hooks
src/views/                      pages: security/ (login, signin), template/ (layout, navbar, sidebar, footer)
src/types/                      API models
security-headers.ts             CSP + headers (dev/preview); mirrored in public/_headers, firebase.json, nginx.conf
```

## Adding a page

1. `src/views/view.<name>.tsx` (default export).
2. Lazy import + `<Route>` in `routing.app.tsx` (inside `ProtectedRoute` if private), link in the sidebar.
3. Data: `services` call + `controllers` function + types in `src/types/`.
4. Test in `src/tests/`, then `make check`.

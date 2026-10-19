# Architecture — {{ cookiecutter.project_name }}

```
src/index.js                 providers (Redux, Router)
src/App.js                   switches between BasicRouting and SecurityRouting
src/routing/                 route tables
src/services/service.api.js  fetch helpers (Send/Get/Update/Remove)
src/controllers/             business logic (validation, toasts)
src/hooks/                   Redux store, reducer, localStorage persistence
src/views/                   pages (security/, template/)
public/                      index.html and static assets
```

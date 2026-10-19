# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Quick start

```bash
make dev-install     # .venv (uv) + deps + dev tools
make run-test        # hot reload on http://localhost:3000  (docs: /docs)
make test lint       # tests + ruff (incl. security rules)
```

A `.env` with random secrets was generated with the project. **Never commit it** (it is in `.gitignore`).
Configuration is typed and validated at startup in `src/{{ cookiecutter.package_slug }}/core/config.py`.

Docker (API{% if cookiecutter.database == 'mongodb' %} + MongoDB{% endif %}{% if cookiecutter.use_redis == 'yes' %} + Redis{% endif %}):

```bash
make dk-up           # docker compose up -d
make dk-logs
```

Run `make help` for every command.

## What is included

| Concern | How |
|---|---|
| Config | `pydantic-settings`, typed, fails fast on missing secrets |
| Auth | JWT (`sub`, `exp`, `role`), `get_current_user`, `require_admin`, owner/admin check (no IDOR) |
| Passwords | Argon2 (`pwdlib`), bcrypt hashes still verified, constant-time login |
| PII | Fernet-encrypted fields + HMAC blind index (`email_hash`) for lookups |
| Rate limit | `slowapi`: global default + strict limit on auth routes{% if cookiecutter.use_redis == 'yes' %}, Redis storage when `REDIS_URL` is set{% endif %} |
| Cache | `fastapi-cache2` ({% if cookiecutter.use_redis == 'yes' %}Redis or {% endif %}in-memory), per-table namespace auto-invalidated on writes |
| Middlewares | request id + access log, security headers (CSP/HSTS/...), body size limit, GZip, CORS, trusted hosts |
| Errors | one JSON shape `{detail, request_id}`, no stack traces leaked |
| Uploads | size limit, type allow-list, magic-bytes check |
| Ops | `/health` (liveness), `/ready` (DB check), JSON logs in prod, multi-stage non-root Docker image |
| Jobs | APScheduler (async) — enable on one instance only (`SCHEDULER_ENABLED`) |

## Production checklist

- `ENVIRONMENT=prod` (disables `/docs`, JSON logs, HSTS)
- `ALLOW_ORIGINS` = your front-end URL(s), never `*`; `ALLOWED_HOSTS` = your domain(s)
- run behind a reverse proxy (TLS) — uvicorn is started with `--proxy-headers`
{%- if cookiecutter.use_redis == 'yes' %}
- set `REDIS_URL` when `WORKERS > 1` (shared cache + rate-limit counters)
{%- else %}
- with `WORKERS > 1` the cache and rate-limit counters are per worker: consider Redis
{%- endif %}
- `make audit` to scan dependencies for CVEs
- create an admin by setting `role: "admin"` directly in the database

## Architecture

```
├── app/main.py                 <- FastAPI app: middlewares, routers, error handlers
├── src/{{ cookiecutter.package_slug }}/
│   ├── core/                   <- config (settings), logging, error handlers
│   ├── data/database.py        <- {{ cookiecutter.database }} access (CRUD + files), normalized results
│   ├── entity/                 <- Entity base class, User, Files (+ pydantic schemas)
│   ├── middleware/             <- http.py (ASGI middlewares), middleware.py (JWT)
│   ├── router/                 <- API routes (user, file, health)
│   └── utils/                  <- cache, limiter, scheduling (lifespan), helpers
├── tests/                      <- pytest (TestClient)
├── Dockerfile, docker-compose.yaml
└── pyproject.toml              <- package + ruff/pytest/mypy config
```


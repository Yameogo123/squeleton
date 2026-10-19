# Architecture — {{ cookiecutter.project_name }}

## Request flow

```
client ─► RequestContext (request id, access log) ─► SecurityHeaders ─► TrustedHost ─► CORS
       ─► BodySizeLimit ─► GZip ─► SlowAPI (rate limit) ─► router ─► entity ─► data/database.py ─► {{ cookiecutter.database }}
errors  ─► core/errors.py  ->  {"detail": ..., "request_id": ...}
startup ─► utils/scheduling.py:lifespan  (cache init, DB connect, scheduler)
```

## Files

```
app/main.py                      FastAPI app: middlewares (order matters: last added = outermost), routers
src/{{ cookiecutter.package_slug }}/
  core/config.py                 Settings (pydantic-settings, .env) — the ONLY config entry point
  core/logging.py                loguru, request id on every line, JSON in prod
  core/errors.py                 global exception handlers
  middleware/http.py             pure ASGI middlewares (request context, security headers, body limit)
  middleware/middleware.py       JWT: signJWT, decodeJWT, get_current_user, require_admin, ensure_owner_or_admin
  data/database.py               {{ cookiecutter.database }}: connect/disconnect/ping, make_crud_action, file_* (normalized results)
  entity/Entity.py               base CRUD class bound to a table
  entity/User.py                 user schemas + business rules (encryption, password policy, login)
  entity/Files.py                upload validation + file responses
  router/r_user.py, r_file.py    HTTP routes
  router/r_health.py             /health (liveness), /ready (DB)
  utils/cache.py                 fastapi-cache2 init + invalidate(namespace)
  utils/limiter.py               slowapi limiter
  utils/scheduling.py            APScheduler jobs + app lifespan
  utils/controller.py            crypto helpers (hash, fernet, blind index), push notifications
tests/                           pytest (conftest sets test env vars)
```

## Adding a resource (e.g. `Product`)

1. Add the table/collection name to `TABLES` in `data/database.py` (+ indexes in `init_indexes`).
2. `entity/Product.py`: pydantic schemas (create/update/out) + `class Product(Entity)` with business rules.
3. `router/r_product.py`: routes with auth + ownership + limits; register it in `app/main.py`.
4. `tests/test_product.py`. Run `make lint && make test`.

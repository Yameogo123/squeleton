# {{ cookiecutter.project_name }} — FastAPI backend

{{ cookiecutter.description }}

Python {{ cookiecutter.python_version }} · FastAPI · {{ cookiecutter.database }}{% if cookiecutter.use_redis == 'yes' %} · Redis{% endif %} · pydantic-settings · JWT · slowapi · fastapi-cache2.
Layout and request flow: see `ARCHITECTURE.md` (read it when you need to locate code).

## Commands

```bash
make dev-install      # .venv + deps (uv)
make run-test         # dev server, hot reload, http://localhost:3000/docs
make test             # pytest            -> single file: .venv/bin/pytest tests/test_api.py -q
make lint             # ruff (incl. bandit security rules)
make format           # ruff format + autofix
make audit            # pip-audit (CVEs in dependencies)
```

**Definition of done** (sanity check, run once before saying "done"): `make lint && make test` both green.

## Conventions

- Config: only through `core/config.py` (`settings`). New variable → `Settings` field + `.env.template` line.
- Layers: router (HTTP only) → entity (business rules + pydantic schemas) → `data/database.py` (driver).
  Routers never call the database driver directly.
- Database results are normalized (`id` as str, counts as int): keep it that way in new code.
- Errors: raise `HTTPException` with a clear message; never return error payloads with 200; never expose
  `str(exception)` to clients (the global handler logs it).
- Every new route: response shape documented by a pydantic model or a dict with stable keys, auth dependency
  (`get_current_user` / `require_admin`), ownership check (`ensure_owner_or_admin`) when it takes an id,
  `@limiter.limit` if it is expensive or auth-related, `@cache(namespace=<table>)` only for safe GET reads.
- Tests in `tests/` with `TestClient`; DB-dependent tests must not need a real database (mock the entity).
- Logging: `from loguru import logger`; never log passwords, tokens or full user documents.

## Security rules

- Passwords: `hash_pwd` / `verify_password` only. PII fields encrypted (`encrypt_text`) + `blind_index` for lookups.
- Never accept `role`, `_id`, `password` hashes or other privileged fields from a client payload.
- Validate all input with pydantic (lengths, `EmailStr`, `Literal`); uploads go through `Files` (type + size + magic bytes).
- Keep CORS origins explicit, `/docs` off in prod, `SECRET_KEY` & co only from the environment.

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

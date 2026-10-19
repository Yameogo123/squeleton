# {{ cookiecutter.project_name }} — ML / data science project

{{ cookiecutter.description }}

Python {{ cookiecutter.python_version }} · installable package in `src/` (`pip install -e .`).
Layout: see `ARCHITECTURE.md` (read it when you need to locate code).

## Commands

```bash
make dev-install      # deps + editable install
make test             # pytest           -> single file: python -m pytest tests/test_x.py -q
make lint             # ruff
make format           # ruff format + autofix
make check            # lint + tests (definition of done)
```

**Definition of done**: `make check` green.

## Conventions

- Library code in `src/{{ cookiecutter.package_slug }}/`, scripts/entry points outside it; scripts only orchestrate.
- Pure functions with type hints and docstrings (numpy style, used by Sphinx); no notebook-only logic.
- Paths via `pathlib`, relative to the project root, never absolute machine paths.
- Logging with `loguru`, never `print` in library code.
- Never commit data or model artifacts: `data/` and model files are gitignored.
- ETL steps are small Dagster ops; each step reads/writes parquet in `data/`.
- Every model training is reproducible: seed, params and metrics logged.

## Security rules

- Never `pickle.load` / `joblib.load` / `torch.load` files from untrusted sources; no `eval`/`exec` on data.
- Validate external inputs (files, API payloads) before processing; bound sizes.
- API (`app/backend`): CORS from env, no secrets in responses or logs.

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

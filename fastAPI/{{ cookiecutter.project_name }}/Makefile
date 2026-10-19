export TERM := xterm

PROJECT_NAME = {{ cookiecutter.project_name }}
PACKAGE_NAME = {{ cookiecutter.package_slug }}
PYTHON_INTERPRETER = {{ cookiecutter.python_interpreter }}
PYTHON_VERSION = {{ cookiecutter.python_version }}
PORT ?= 3000
WORKERS ?= 2

VENV = .venv
PYTHON = $(VENV)/bin/python
UVICORN = $(VENV)/bin/uvicorn

ccend = $(shell tput sgr0)
ccso = $(shell tput smso)

.DEFAULT_GOAL := help
.PHONY: help venv install dev-install prod-install run-app run run-test lint format typecheck test cov audit \
        clean env dk-build dk-up dk-down dk-logs conda_env pyenv_env uv_env delete_pyenv_env git-push git-publish

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

# ------------------------------------------------------------------ setup
venv: ## Create the .venv with uv
	@test -d $(VENV) || uv venv $(VENV) --python $(PYTHON_VERSION)

install: venv ## Install prod dependencies + the package (editable)
	uv pip install --python $(PYTHON) -r requirements.txt -e .

dev-install: venv ## Install prod + dev dependencies and git hooks
	uv pip install --python $(PYTHON) -r requirements.txt -r requirements-dev.txt -e .
	@[ -d .git ] && $(VENV)/bin/pre-commit install || echo "--> run 'git init' then '$(VENV)/bin/pre-commit install' to enable git hooks"

prod-install: ## Install in the current interpreter (servers without venv)
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt .

env: ## Create .env from .env.template if missing
	@test -f .env || (cp .env.template .env && echo "--> .env created, fill in the secrets")

# ------------------------------------------------------------------ run
run-test: ## Dev server with hot reload
	$(UVICORN) app.main:app --reload --port $(PORT)

run-app: run-test

run: ## Production-like server (multi workers, proxy headers)
	$(UVICORN) app.main:app --host 0.0.0.0 --port $(PORT) --workers $(WORKERS) --proxy-headers --no-server-header

prod-backend: install run ## venv + install + run

# ------------------------------------------------------------------ quality
lint: ## Lint (ruff, incl. security rules)
	$(VENV)/bin/ruff check src app tests

format: ## Format + autofix
	$(VENV)/bin/ruff format src app tests
	$(VENV)/bin/ruff check --fix src app tests

typecheck: ## mypy
	$(VENV)/bin/mypy src

test: ## Run tests
	$(VENV)/bin/pytest

cov: ## Tests with coverage report
	$(VENV)/bin/pytest --cov --cov-report=term-missing

audit: ## Scan dependencies for known vulnerabilities
	$(VENV)/bin/pip-audit -r requirements.txt

clean: ## Remove caches
	find . -type d \( -name "__pycache__" -o -name ".pytest_cache" -o -name ".ruff_cache" -o -name ".mypy_cache" \) -prune -exec rm -rf {} +

# ------------------------------------------------------------------ docker
dk-build: ## Build the image
	docker compose build

dk-up: env ## Start the stack
	docker compose up -d

dk-down: ## Stop the stack
	docker compose down

dk-logs: ## Follow API logs
	docker compose logs -f api

# ------------------------------------------------------------------ other envs
uv_env: ## uv sync (uses pyproject)
	uv sync

conda_env: ## Create a conda env
	conda create --name $(PACKAGE_NAME) python=$(PYTHON_VERSION)
	@echo ">>> Activate with: conda activate $(PACKAGE_NAME)"

pyenv_env: ## Create a pyenv virtualenv
	pyenv virtualenv $(PYTHON_VERSION) $(PACKAGE_NAME)
	pyenv local $(PACKAGE_NAME)

delete_pyenv_env: ## Delete the pyenv virtualenv
	pyenv virtualenv-delete $(PACKAGE_NAME)

git-push: ## add + commit + push (asks for a message)
	@read -p "Message: " msg; git add .; git commit -m "$$msg"; git push

git-publish: git-push ## push to the deploy remote (edit the URL)
	git push git@git.evennode.com:xxxxx.com dev:master
	git push origin dev

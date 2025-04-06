
export TERM := xterm

# Variables
DOCKER_COMPOSE = docker-compose
MONGO_SERVICE = mongo

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = {{ cookiecutter.project_name }}
PACKAGE_NAME = {{ cookiecutter.package_slug }}
PYTHON_INTERPRETER = python3
PYTHON_VERSION = {{ cookiecutter.python_version }}


VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
APP_DIR = app


# echo colors
ccend = $(shell tput sgr0)
ccbold = $(shell tput bold)
ccgreen = $(shell tput setaf 2)
ccred = $(shell tput setaf 1)
ccso = $(shell tput smso)


# Run FastAPI (using absolute paths)
run-app:
	@echo "--> Starting FastAPI"
	$(PYTHON_INTERPRETER) -m uvicorn app.main:app --port $(PORT)


venv:
	@echo "--> Creating virtual environment"
	python3 -m venv $(VENV)

# Install dependencies
install:
	@echo "--> Installing dependencies"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

# Run FastAPI (using absolute paths)
run:
	@echo "--> Starting FastAPI"
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port $(PORT)


prod-backend: venv install run


ifeq (,$(shell which conda))
HAS_CONDA = False
else
HAS_CONDA = True
endif

ifeq (,$(shell which pyenv))
HAS_PYENV = False
else
HAS_PYENV = True
endif

ifeq (,$(shell which poetry))
HAS_POETRY = False
else
HAS_POETRY = True
endif


clean:
	@echo "$(ccso)--> Delete all compile python files $(ccend)"
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


dev-install:
	@echo "$(ccso) --> Install Python Dependencies (DEV)$(ccend)"
	$(PYTHON_INTERPRETER) -m pip install uv
	$(PYTHON_INTERPRETER) -m uv pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m uv pip install --upgrade pip
	$(PYTHON_INTERPRETER) -m uv pip install -r requirements-dev.txt
	$(PYTHON_INTERPRETER) -m uv pip install -r requirements.txt
	$(PYTHON_INTERPRETER) -m uv pip install -e .

prod-install:
	@echo "$(ccso) --> Install Python Dependencies (PROD)$(ccend)"
	$(PYTHON_INTERPRETER) -m pip install uv
	$(PYTHON_INTERPRETER) -m uv pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m uv pip install --upgrade pip
	$(PYTHON_INTERPRETER) -m uv pip install -r requirements.txt
	$(PYTHON_INTERPRETER) -m uv pip install .



conda_env:
	@echo "$(ccso)--> Set up python interpreter environment (conda)$(ccend)"
ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda create --name $(PACKAGE_NAME) python=3
else
	conda create --name $(PACKAGE_NAME) python=2.7
endif
	@echo ">>> New conda env created. Activate with:\nsource activate $(PACKAGE_NAME)"
else
	@echo ">>> No virtualenv packages installed. Please install one above first"
endif

## Set up python interpreter environment (pyenv)
pyenv_env:
	@echo "$(ccso)--> Set up python interpreter environment (pyenv)$(ccend)"
ifeq (True,$(HAS_PYENV))
	@echo ">>> Detected pyenv, creating pyenv environment."
	pyenv virtualenv $(PYTHON_VERSION) $(PACKAGE_NAME)
	@echo ">>> New pyenv created. Activate with: pyenv activate $(PACKAGE_NAME)"
	pyenv local $(PACKAGE_NAME) 
	@echo ">>> By default, the pyenv is activated in the local folder"
else
	@echo ">>> No virtualenv packages installed. Please install one above first"
endif

## Delete pyenv environment
delete_pyenv_env:
	@echo "$(ccso)--> Delete pyenv environment$(ccend)"
	pyenv virtualenv-delete $(PACKAGE_NAME)
	@echo "Fichier $(TEMPLATE_FILE) créé avec succès"


# Default target
all: build

# Build all Docker services
dk-build:
	@echo "Building Docker images..."
	$(DOCKER_COMPOSE) build

# Start all services in detached mode
dk-up:
	@echo "Starting services..."
	$(DOCKER_COMPOSE) up -d

# Stop all services
dk-down:
	@echo "Stopping services..."
	$(DOCKER_COMPOSE) down

# Restart all services
dk-restart: dk-down dk-up

# View logs for all services
logs:
	@echo "Showing logs..."
	$(DOCKER_COMPOSE) logs -f

# View logs for a specific service (e.g., make logs-backend)
logs-%:
	@echo "Showing logs for $*..."
	$(DOCKER_COMPOSE) logs -f $*

# Access the backend container shell
backend-shell:
	@echo "Accessing backend container shell..."
	$(DOCKER_COMPOSE) exec $(BACKEND_SERVICE) /bin/bash

# Access the frontend container shell
frontend-shell:
	@echo "Accessing frontend container shell..."
	$(DOCKER_COMPOSE) exec $(FRONTEND_SERVICE) /bin/bash

# Access the MongoDB container shell
mongo-shell:
	@echo "Accessing MongoDB container shell..."
	$(DOCKER_COMPOSE) exec $(MONGO_SERVICE) mongosh -u root -p example

# Clean up Docker resources (containers, networks, volumes)
dk-clean:
	@echo "Cleaning up Docker resources..."
	$(DOCKER_COMPOSE) down --volumes --remove-orphans

# Help command to list all available targets
help:
	@echo "Available targets:"
	@echo "  dk-build         - Build all Docker images"
	@echo "  dk-up            - Start all services in detached mode"
	@echo "  dk-down          - Stop all services"
	@echo "  restart       - Restart all services"
	@echo "  logs          - View logs for all services"
	@echo "  logs-<service> - View logs for a specific service (e.g., logs-backend)"
	@echo "  backend-shell - Access the backend container shell"
	@echo "  frontend-shell - Access the frontend container shell"
	@echo "  mongo-shell   - Access the MongoDB container shell"
	@echo "  dk-clean         - Clean up Docker resources (containers, networks, volumes)"
	@echo "  help          - Show this help message"

# Default target
.PHONY: all build up down restart logs logs-% backend-shell frontend-shell mongo-shell clean help
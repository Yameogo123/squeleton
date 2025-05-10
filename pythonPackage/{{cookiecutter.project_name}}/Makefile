# Variables
DOCKER_COMPOSE = docker-compose
BACKEND_SERVICE = backend
FRONTEND_SERVICE = frontend
MONGO_SERVICE = mongo

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = {{ cookiecutter.project_name }}
PACKAGE_NAME = {{ cookiecutter.package_slug }}
PYTHON_INTERPRETER = python3
PYTHON_VERSION = {{ cookiecutter.python_version }}
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = ./docs/{{ cookiecutter.package_slug }}_docs
BUILDDIR      = ./docs/{{ cookiecutter.package_slug }}/_build


# echo colors
ccend = $(shell tput sgr0)
ccbold = $(shell tput bold)
ccgreen = $(shell tput setaf 2)
ccred = $(shell tput setaf 1)
ccso = $(shell tput smso)




run_app_front:
	@echo "$(ccso)--> Run the streamlit demo app $(ccend)"
	cd app/frontend && streamlit run app.py

run_app_back:
	@echo "$(ccso)--> Run the fastAPI demo app $(ccend)"
	cd app/backend && python main.py

run:
	@echo "$(ccso)--> Run the script demo $(ccend)"
	cd src && python main_script.py



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

test_environment:
	@echo "$(ccso) --> Test de la presence d'environnement python$(ccend)"
	$(PYTHON_INTERPRETER) ./tests/test_environment.py
ifeq (True, $(HAS_CONDA))
	@echo ">>> Conda is $(ccgreen)available $(ccend)"
else
	@echo ">>> Conda is $(ccred)not available $(ccend)"
endif
ifeq (True, $(HAS_PYENV))
	@echo ">>> Pyenv is $(ccgreen)available $(ccend)"
else
	@echo ">>> Pyenv is $(ccred)not available $(ccend)"
endif
ifeq (True, $(HAS_POETRY))
	@echo ">>> Poetry is $(ccgreen)available $(ccend)"
else
	@echo ">>> Poetry is $(ccred)not available $(ccend)"
endif


dev-install: test_environment
	@echo "$(ccso) --> Install Python Dependencies (DEV)$(ccend)"
	$(PYTHON_INTERPRETER) -m pip install uv
	$(PYTHON_INTERPRETER) -m uv pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m uv pip install --upgrade pip
	$(PYTHON_INTERPRETER) -m uv pip install -r requirements-dev.txt
	$(PYTHON_INTERPRETER) -m uv pip install -r requirements.txt
	$(PYTHON_INTERPRETER) -m uv pip install -e ".[dev]"

prod-install: test_environment
	@echo "$(ccso) --> Install Python Dependencies (PROD)$(ccend)"
	$(PYTHON_INTERPRETER) -m pip install uv
	$(PYTHON_INTERPRETER) -m uv pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m uv pip install --upgrade pip
	$(PYTHON_INTERPRETER) -m uv pip install -r requirements.txt
	$(PYTHON_INTERPRETER) -m uv pip install -e .



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



###############################################


## Delete all compiled _build/ folder
sphinx-clean:
	@echo "Delete _build directory"
	rm -r "$(BUILDDIR)"

## Automatically generate HTML documentation
sphinx-livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) --port=8001




#################################################################################
# UTILITIES                                                                 #
#################################################################################

## Auto-generate the rst file for the Sphinx documentation
generate_docs:
	@echo "$(ccso)--> Generate the RST file for the Sphinx documentation$(ccend)"
	sphinx-apidoc -o ./docs src/
	@echo "RST files are available at: ./docs/"

# Create the .env-template from .env
create-env-template: $(ENV_FILE)
	@echo "$(ccso)--> Create the template file $(TEMPLATE_FILE) from $(ENV_FILE)$(ccend)"
	@awk -F'=' '{print $$1"=\"\""}' $(ENV_FILE) > $(TEMPLATE_FILE)
	@echo "Fichier $(TEMPLATE_FILE) créé avec succès"


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
	@echo "  run_app_front    - Run the Streamlit demo app"
	@echo "  run_app_back     - Run the FastAPI demo app"
	@echo "  run              - Run the script demo"
	@echo "  clean            - Delete all compiled Python files"
	@echo "  test_environment - Test the presence of Python environment tools"
	@echo "  dev-install      - Install Python dependencies for development"
	@echo "  prod-install     - Install Python dependencies for production"
	@echo "  conda_env        - Set up Python interpreter environment using Conda"
	@echo "  pyenv_env        - Set up Python interpreter environment using Pyenv"
	@echo "  delete_pyenv_env - Delete the Pyenv environment"
	@echo "  sphinx-clean     - Delete the Sphinx _build directory"
	@echo "  sphinx-livehtml  - Automatically generate live HTML documentation"
	@echo "  generate_docs    - Auto-generate RST files for Sphinx documentation"
	@echo "  create-env-template - Create a .env-template from .env"
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
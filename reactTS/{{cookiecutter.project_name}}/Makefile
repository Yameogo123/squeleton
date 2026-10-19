IMAGE = {{ cookiecutter.project_slug }}
NODE_VERSION = $(shell cat .nvmrc)

ccend = $(shell tput sgr0)
ccso = $(shell tput smso)

.DEFAULT_GOAL := help
.PHONY: help use-node install ci dev run build preview lint typecheck test check audit clean docker-build docker-run firebase-deploy git-push

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

use-node: ## Install/use the Node version from .nvmrc (nvm)
	@. "$$HOME/.nvm/nvm.sh" && nvm install $(NODE_VERSION) && nvm use $(NODE_VERSION)

install: ## npm install (creates/updates package-lock.json: commit it)
	npm install

ci: ## Reproducible install from package-lock.json (CI / servers)
	npm ci

dev: ## Dev server on http://localhost:5173
	npm run dev

run: dev

build: ## Type-check + production build (dist/)
	npm run build

preview: build ## Serve the build with production security headers
	npm run preview

lint: ## oxlint
	npm run lint

typecheck: ## tsc
	npm run typecheck

test: ## vitest
	npm test

check: lint typecheck test ## lint + types + tests

audit: ## Known vulnerabilities in prod dependencies
	npm run audit

clean: ## Remove build outputs
	rm -rf dist coverage node_modules/.vite node_modules/.tmp

docker-build: ## Build the nginx image (VITE_API_URL from .env.local)
	docker build --build-arg VITE_API_URL=$$(grep VITE_API_URL .env.local | cut -d= -f2) -t $(IMAGE) .

docker-run: ## Run the image on http://localhost:8080
	docker run --rm -p 8080:8080 $(IMAGE)

firebase-deploy: build ## Deploy dist/ to Firebase Hosting (edit the target)
	npx firebase-tools deploy --only hosting:xxxxx

git-push: ## add + commit + push (asks for a message)
	@read -p "Message: " msg; git add .; git commit -m "$$msg"; git push

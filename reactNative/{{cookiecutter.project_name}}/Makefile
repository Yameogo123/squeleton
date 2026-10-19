NODE_VERSION = $(shell cat .nvmrc)

.DEFAULT_GOAL := help
.PHONY: help use-node install start ios android web lint typecheck test check doctor fix-deps clean build-dev build-preview

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

use-node: ## Install/use the Node version from .nvmrc (nvm)
	@. "$$HOME/.nvm/nvm.sh" && nvm install $(NODE_VERSION) && nvm use $(NODE_VERSION)

install: ## npm install (commit package-lock.json)
	npm install

start: ## Expo dev server (scan the QR code with Expo Go / dev build)
	npx expo start

ios: ## iOS simulator
	npx expo start --ios

android: ## Android emulator
	npx expo start --android

web: ## Web
	npx expo start --web

lint: ## expo lint
	npm run lint

typecheck: ## tsc
	npm run typecheck

test: ## jest
	npm test

check: lint typecheck test ## lint + types + tests

doctor: ## Diagnose dependency / config issues
	npx expo-doctor

fix-deps: ## Align packages on the SDK versions (use instead of npm install <pkg>)
	npx expo install --fix

clean: ## Clear Metro / Expo caches
	rm -rf .expo node_modules/.cache && npx expo start --clear

build-dev: ## EAS development build
	npx eas-cli@latest build --profile development

build-preview: ## EAS internal preview build
	npx eas-cli@latest build --profile preview

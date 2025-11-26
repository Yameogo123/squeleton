# Variables
PROJECT_NAME = {{ cookiecutter.project_name }}
# Node.js version to install
NODE_VERSION = {{ cookiecutter.node_version }}  # Change this to the version you need
# NVM install script URL
NVM_INSTALL_URL = {{ cookiecutter.nvm_url }}

# echo colors
ccend = $(shell tput sgr0)
ccbold = $(shell tput bold)
ccgreen = $(shell tput setaf 2)
ccred = $(shell tput setaf 1)
ccso = $(shell tput smso)

.PHONY: install-nvm install-node use-node install-packages clean-node


# 1- Install NVM if not exists
install-nvm:
	@echo "$(ccso)--> 🔍 Checking if NVM is installed... $(ccend)"
	@if ! command -v nvm &> /dev/null; then \
		echo "$(ccso)--> ⚡ Installing NVM... $(ccend)"; \
		curl -o- $(NVM_INSTALL_URL) | bash; \
		export NVM_DIR="$$HOME/.nvm"; \
		[ -s "$$NVM_DIR/nvm.sh" ] && \. "$$NVM_DIR/nvm.sh"; \
		echo "$(ccso)--> ✅ NVM installed! Restart your terminal or run: source $$HOME/.nvm/nvm.sh $(ccend)"; \
	else \
		echo "$(ccso)--> ✅ NVM is already installed. $(ccend)"; \
	fi

# 2- Install Node.js & npm using nvm
install-node:
	@echo "$(ccso)--> Installing Node.js $(NODE_VERSION) using nvm... $(ccend)"
	@if [ -d "$$HOME/.nvm" ]; then \
		source $$HOME/.nvm/nvm.sh && nvm install $(NODE_VERSION); \
	else \
		echo "$(ccso)--> ❌ NVM not found. Please install nvm first. $(ccend)"; \
	fi

# 3- Use the installed Node.js version
use-node:
	@echo "$(ccso)--> Setting Node.js version $(NODE_VERSION)... $(ccend)"
	@if [ -d "$$HOME/.nvm" ]; then \
		source $$HOME/.nvm/nvm.sh && nvm use $(NODE_VERSION); \
	else \
		echo "$(ccso)--> ❌ NVM not found. Please install nvm first. $(ccend)"; \
	fi

# 4- Install npm packages
install-packages:
	@echo "$(ccso)--> Installing npm packages... $(ccend)"
	@if [ -d "$$HOME/.nvm" ]; then \
		source $$HOME/.nvm/nvm.sh && nvm use $(NODE_VERSION) && npm install; \
	else \
		echo "$(ccso)--> ❌ NVM not found. Please install nvm first. $(ccend)"; \
	fi

# Remove Node.js version
clean-node:
	@echo "$(ccso)--> Removing Node.js $(NODE_VERSION)... $(ccend)"
	@if [ -d "$$HOME/.nvm" ]; then \
		source $$HOME/.nvm/nvm.sh && nvm uninstall $(NODE_VERSION); \
	else \
		echo "$(ccso)--> ❌ NVM not found. Please install nvm first. $(ccend)"; \
	fi


# 1 + 2 + 3 + 4 - Default target: Runs all necessary steps in sequence
all-install: install-nvm install-node use-node install-packages

# to launch the script
run: 
	@echo "$(ccso)--> Running the script $(ccend)"
	npm start


git-push:
	@echo "Enter commit message:"
	@read -p "Message: " msg; \
	git add .; \
	git commit -m "$$msg"; \
	git push
# 🍪 CookieCutter Skeleton Templates

A collection of project templates to kickstart your development with proper structure and best practices.

## 📋 Requirements

### Node.js Projects
- **Node.js** and **npm** installed on your computer

### Python Projects  
- **Python** installed on your computer

### CookieCutter Installation
```bash
# Via npm
npm install -g cookiecutter

# Or via pip
pip install cookiecutter
```

## 🚀 Available Templates

### 0. 🐍 Simple Python Package
For all Python package development

```bash
cookiecutter https://github.com/Yameogo123/squeleton.git --directory="pythonPackage"
```

### 1. ⚡ FastAPI Application  
For FastAPI applications using Python packaging system: typed settings, JWT + RBAC, rate limiting,
cache (Redis / in-memory), security middlewares, health checks, Docker, tests

```bash
cookiecutter https://github.com/Yameogo123/squeleton.git --directory="fastAPI"
```

### 2. 🤖 ML Project
For Machine Learning projects in Python (using packaging)

```bash
cookiecutter https://github.com/Yameogo123/squeleton.git --directory="ML"
```

### 3. ⚛️ React + TypeScript Project (recommended)
React 19 + TypeScript + Vite, Redux Toolkit, React Router, Tailwind 4, Vitest, security headers (CSP)

```bash
cookiecutter https://github.com/Yameogo123/squeleton.git --directory="reactTS"
```

### 3bis. ⚛️ ReactJS Project (legacy, Create React App)
Kept for existing projects. Create React App is deprecated: prefer `reactTS` for new ones.

```bash
cookiecutter https://github.com/Yameogo123/squeleton.git --directory="reactJS"
```

### 4. 📱 React Native Project (Expo)
Expo SDK 58 + TypeScript: login, signup, bottom tabs (Accueil, Messages, Réglages), design system with
light/dark tokens, secure token storage, tests

```bash
cookiecutter https://github.com/Yameogo123/squeleton.git --directory="reactNative"
```


---

## 🎯 Usage Example

1. Choose your template from the list above
2. Run the corresponding cookiecutter command
3. Follow the interactive prompts to configure your project
4. Start coding with a well-structured foundation!

## 🤖 Claude Code, pre-configured

Every generated project ships with Claude Code config tuned for its stack:

| File | Purpose |
|---|---|
| `CLAUDE.md` | commands, conventions, security rules, token-economy rules (loaded every session, kept short) |
| `ARCHITECTURE.md` | layout + "how to add a resource/page/screen" (read on demand) |
| `.claude/settings.json` | permissions: common checks allowed, secrets/lockfiles/deps denied, risky git commands ask |
| `.claude/hooks/protect-secrets` | blocks any read/edit/grep/shell access to `.env*`, keys, credentials |
| `.claude/hooks/lint-changed` | lints only the file Claude just edited and sends errors back immediately |
| `.claude/agents/` | `code-reviewer`, `security-auditor` (+ `ui-ux-reviewer` for front ends), on Sonnet to save tokens |
| `.claude/commands/` | `/check` (sanity check), `/review`, `/secure`, plus a scaffolder (`/new-resource`, `/new-page`, `/new-screen`, ...) |

Personal overrides go in `.claude/settings.local.json` / `CLAUDE.local.md` (gitignored).

## 📁 Template Features

Each template includes:
- ✅ Proper project structure
- ✅ Configuration files
- ✅ Development environment setup
- ✅ Best practices implementation
- ✅ Ready-to-use build systems

---

*Start your projects faster with standardized templates!* 🚀
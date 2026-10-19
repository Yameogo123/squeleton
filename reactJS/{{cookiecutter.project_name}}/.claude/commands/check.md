---
description: Sanity check — eslint + tests (definition of done)
allowed-tools: Bash(npx eslint:*), Bash(CI=true npm test:*)
---
Run `npx eslint src` then `CI=true npm test -- --watchAll=false`.
- Green → one line: "✅ lint + tests OK".
- Failures → show only failing items (file:line + message), fix, re-run until green.

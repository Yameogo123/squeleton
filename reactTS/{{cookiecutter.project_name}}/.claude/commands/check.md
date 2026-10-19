---
description: Sanity check — lint + typecheck + tests (definition of done)
allowed-tools: Bash(make check), Bash(npm run lint), Bash(npm run typecheck), Bash(npm test)
---
Run `make check`.
- Green → one line: "✅ lint + types + tests OK".
- Failures → show only the failing items (file:line + message), fix them, re-run, repeat until green.

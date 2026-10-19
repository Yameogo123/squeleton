---
description: Sanity check — lint + typecheck + tests (definition of done)
allowed-tools: Bash(npm run check), Bash(npm run lint), Bash(npm run typecheck), Bash(npm test)
---
Run `npm run check`.
- Green → one line: "✅ lint + types + tests OK".
- Failures → show only failing items (file:line + message), fix, re-run, repeat until green.

---
description: Sanity check — lint + tests (definition of done)
allowed-tools: Bash(make check), Bash(make lint), Bash(make test)
---
Run `make check`.
- Green → one line: "✅ lint + tests OK".
- Failures → show only the failing items (file:line + message), fix them, re-run, repeat until green.

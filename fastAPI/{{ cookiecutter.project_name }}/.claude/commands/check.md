---
description: Sanity check — lint + tests (definition of done)
allowed-tools: Bash(make lint), Bash(make test)
---
Run `make lint` then `make test`.
- All green → answer with one line: "✅ lint + tests OK".
- Failures → show only the failing items (file:line + message), fix them, re-run the failing step, and
  repeat until green. Don't paste full logs.

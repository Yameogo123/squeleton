---
description: Scaffold a new page (view + route + data + test) following the project conventions
argument-hint: <page name and purpose>
---
Create the page: $ARGUMENTS — following `ARCHITECTURE.md` → "Adding a page".
- Tailwind, mobile-first, semantic HTML, loading/empty/error states.
- Typed service + controller if it loads data.
- One Testing Library test (renders + main interaction).
Then use the **ui-ux-reviewer** subagent on the new files, apply 🔴/🟠 findings, and run `/check`.

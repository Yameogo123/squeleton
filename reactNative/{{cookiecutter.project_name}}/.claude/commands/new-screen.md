---
description: Scaffold a new mobile screen (route + UI + data + test) calibrated on the design system
argument-hint: <screen name, tab or stack, purpose>
---
Create the screen: $ARGUMENTS — following `ARCHITECTURE.md` → "Adding a screen".
- `<Screen>` wrapper, `components/ui/*` only, tokens via `useTheme()`; loading / empty / error states.
- Data through a typed function in `src/services/`.
- Accessibility: roles + labels, targets ≥ `HitSize`, works in dark mode and with large fonts.
- One test in `src/__tests__/` (renders + main interaction).
Then use the **ui-ux-reviewer** subagent on the new files, apply 🔴/🟠 findings, and run `/check`.

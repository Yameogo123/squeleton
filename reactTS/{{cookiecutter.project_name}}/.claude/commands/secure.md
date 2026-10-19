---
description: Security audit of the project or of a given path
---
Use the **security-auditor** subagent on `$ARGUMENTS` (default: the whole project, prioritizing recent changes
from `git diff HEAD`).

Report only real, exploitable issues ranked by severity, each with `file:line`, the attack scenario in one
sentence, and the fix. No generic advice. Do not apply fixes unless I ask.

---
description: Expert review of the current changes (bugs, security, performance, conventions)
---
Use the **code-reviewer** subagent to review the current changes.

Scope: `$ARGUMENTS` if given (file, folder, branch or commit), otherwise `git diff HEAD` + untracked files.

Give it only the list of changed files and the scope; it reads what it needs.
Then report its findings to me ranked by severity (🔴 must fix / 🟠 should fix / 🟡 nit), each with
`file:line`, the problem in one sentence and the concrete fix. Do not apply fixes unless I ask.

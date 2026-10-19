#!/usr/bin/env python3
"""PostToolUse hook: after Claude edits a Python file, autofix + lint THAT file only (fast, cheap).

Remaining lint errors are sent back to Claude (exit 2) so it fixes them right away.
Silently does nothing when ruff isn't installed yet.
"""
import json
import os
import shutil
import subprocess
import sys

event = json.load(sys.stdin)
path = (event.get("tool_input") or {}).get("file_path", "")
if not path.endswith(".py") or not os.path.exists(path):
    sys.exit(0)

project = os.environ.get("CLAUDE_PROJECT_DIR", ".")
ruff = os.path.join(project, ".venv", "bin", "ruff")
ruff = ruff if os.path.exists(ruff) else shutil.which("ruff")
if not ruff:
    sys.exit(0)

# run from the project root so ruff uses pyproject.toml
run = dict(capture_output=True, text=True, cwd=project)
subprocess.run([ruff, "check", "--fix", "--quiet", path], **run)
subprocess.run([ruff, "format", "--quiet", path], **run)
result = subprocess.run([ruff, "check", "--output-format=concise", path], **run)
if result.returncode != 0:
    print(f"ruff found issues in {path}:\n{result.stdout.strip()[:2000]}", file=sys.stderr)
    sys.exit(2)

#!/usr/bin/env python3
"""PreToolUse hook: never let Claude read, print, edit or grep secret files.

Exit code 2 blocks the tool call and shows the reason to Claude.
Templates such as .env.example / .env.template stay readable (they hold no values).
"""
import json
import re
import sys

ALLOWED = re.compile(r"\.env\.(example|template|sample|dist)$")
SECRET = re.compile(
    r"(?:(?<=[\\/\s'\"=])|^)("
    r"\.env(\.[\w.-]+)?"
    r"|[\w.-]+\.(pem|key|p8|p12|pfx|jks|keystore|mobileprovision)"
    r"|id_(rsa|ed25519|ecdsa)[\w.-]*"
    r"|credentials\.json|service-account[\w.-]*\.json|google-services\.json|GoogleService-Info\.plist"
    r")(?=$|[\s'\";|&)<>])"
)


def secret_in(text: str) -> str | None:
    for match in SECRET.finditer(text or ""):
        name = match.group(1)
        if not ALLOWED.search(name):
            return name
    return None


def main() -> None:
    event = json.load(sys.stdin)
    tool = event.get("tool_name", "")
    data = event.get("tool_input", {}) or {}
    if tool == "Bash":
        candidates = [data.get("command", "")]
    else:
        # Grep's search *pattern* is not checked: searching code for "process.env" is fine
        candidates = [str(data.get(k, "")) for k in ("file_path", "path", "notebook_path", "glob")]
    for text in candidates:
        hit = secret_in(" " + text + " ")
        if hit:
            print(
                f"Blocked by .claude/hooks: '{hit}' is a secrets file. Do not read, print, copy or edit it. "
                "Use the .env.template / .env.example file for variable names, and ask the user to set values.",
                file=sys.stderr,
            )
            sys.exit(2)


if __name__ == "__main__":
    main()

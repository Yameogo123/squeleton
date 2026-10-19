"""Runs inside the generated project: keeps the chosen database module and creates a .env with fresh secrets."""
import base64
import os
import secrets
from pathlib import Path

database_choice = "{{ cookiecutter.database }}"
package_slug = "{{ cookiecutter.package_slug }}"

data_dir = Path("src") / package_slug / "data"
for db in ("mongodb", "supabase"):
    path = data_dir / f"db_{db}.py"
    if db == database_choice:
        path.rename(data_dir / "database.py")
    elif path.exists():
        path.unlink()

# .env with real random secrets (never committed: see .gitignore)
template = Path(".env.template").read_text()
fernet_key = base64.urlsafe_b64encode(os.urandom(32)).decode()
generated = {
    "SECRET_KEY": secrets.token_urlsafe(64),
    "FERNET_KEY": fernet_key,
    "BLIND_INDEX_KEY": secrets.token_urlsafe(32),
}
lines = []
for line in template.splitlines():
    key = line.split("=", 1)[0].strip()
    lines.append(f"{key}={generated[key]}" if key in generated and not line.startswith("#") else line)
env_file = Path(".env")
env_file.write_text("\n".join(lines) + "\n")
env_file.chmod(0o600)

print(f"""
  Project generated with {database_choice}.
  A .env with fresh secrets was created (keep it out of git).

  Next steps:
    cd {{ cookiecutter.project_name }}
    make dev-install
    make run-test        # http://localhost:3000/docs
""")

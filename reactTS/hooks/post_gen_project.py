import shutil
from pathlib import Path

# local env file for dev (gitignored); .env.example stays as documentation
if not Path(".env.local").exists():
    shutil.copy(".env.example", ".env.local")

print("""
  Project generated. Next steps:
    cd {{ cookiecutter.project_name }}
    make install   # or: npm install
    make dev       # http://localhost:5173
""")

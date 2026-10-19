# Architecture — {{ cookiecutter.project_name }}

```
src/{{ cookiecutter.package_slug }}/     the package (imported everywhere, tested)
  data/, features/, models/      domain sub-packages
  utils/                         reader, helpers
app/backend/main.py              FastAPI API exposing results (/health)
app/frontend/                    Streamlit app (pages in _pages/, menu in pages_sections.toml)
data/raw → interm → processed    data lifecycle (gitignored)
notebooks/                       exploration only — move reusable code into src/
docs/                            Sphinx documentation (make docs-install, make generate_docs)
tests/                           pytest
```

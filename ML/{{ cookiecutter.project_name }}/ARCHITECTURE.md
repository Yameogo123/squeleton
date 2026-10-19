# Architecture — {{ cookiecutter.project_name }}

```
src/{{ cookiecutter.package_slug }}/     the package (imported everywhere, tested)
  features/etl/                  extract → transform → load (Dagster job in src/main_etl.py)
  data/quality, data/analysis    data checks and descriptive analysis
  models/autoML                  supervised / unsupervised / time series AutoML
  utils/                         reader (files → DataFrames), helpers
app/backend/main.py              FastAPI API exposing results (/health)
app/frontend/                    Streamlit app (pages in _pages/, menu in pages_sections.toml)
data/raw → interm → processed    data lifecycle (gitignored)
notebooks/                       exploration only — move reusable code into src/
docs/                            Sphinx documentation (make docs-install, make generate_docs)
tests/                           pytest
```

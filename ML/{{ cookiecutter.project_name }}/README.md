# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

### steps:

#### 1. requirements: 
- you need, of course, to install python on your computer.
- you need then to install cookiecutter on python `pip install cookiecutter`

#### 2. prepare environment:

Use pyenv or conda env

- Create pyenv environnemment (or conda env : conda_env)
```bash
   make pyenv_env
```

- If not activate: activate the env created (do it yourself)

- Install the requirements next:
```bash
   make dev-install
```

(**Optionnal**) you can use a venv if you want.


(The rest of the command are in the makefile. You can open it to see.)

#### 3. the squeleton 

```
---
├── LICENSE
├── Makefile
├── README.md          <- The top-level README for developers using this project.
├── app                <- Web / Streamlit app for demo
│   ├── frontend       <- contain the frontend of the app (in streamlit).
│   └── backend        <- a fastAPI app to expose your results as API.
├── data
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default Sphinx project; see sphinx-doc.org for details
│
├── models             <- Trained and serialized models, model predictions
│
├── notebooks          <- Jupyter notebooks.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.py           <- makes installable (pip install -e .) so src can be imported
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── features       <- for engineering
│   │    ├── etl       <- Scripts to transform data
│   │    └──
│   │
│   ├── data           <- Scripts for data quality
│   │    ├── quality
│   │    └── visualization
│   │
│   ├── models         <- Scripts to train models and use them for predictions
│   │    ├── MLOps
│   │    └── autoML
│   │
│   └── visualization  <- Scripts to create exploratory and results oriented visualizations
│       └── visualize.py
│
├── tests               <- to test the functions
|
└── docker-compose.yaml         <- to dockerize front and back end
---
```

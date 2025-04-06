# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Run in CMD

1. Use pyenv or conda env

- Create pyenv environnemment (or conda env : conda_env)
```bash
   make pyenv_env
```

- If not activate: activate the env created (do it yourself)

- Install the requirements next:
```bash
   make dev-install
```

- Run the app
```bash
   make run-app
```

2. (Optionnal) you can use a venv instead:
- init venv
```bash
   make venv
```
- install packages in it
```bash
   make install
```
- run the API app
```bash
   make run
```

or run the 3 with one command:
```bash
   make prod-backend
```


3. you can also use docker:
check the MakeFile


## the project architecture

```
---
├── Makefile
├── README.md          <- The top-level README for developers using this project.
├── app                <- a fastAPI app to expose your results as API.
│
├── requirements.txt   <- The requirements file for the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── pyproject.toml          <- makes installable (pip install -e .)
├── src                     <- Source code for use in this project.
│    ├── {{ cookiecutter.package_slug }}     <- package
│    │   ├── __init__.py    <- Makes src a Python module
│    │   │
│    │   ├── data           <- Scripts for database connections
│    │   │    └── mongodb.py
│    │   │
│    │   ├── entity         <- all the entities of UML
│    │   │    ├── Entity.py <- abstract class that will be used in the others
│    │   │    └── *
│    │   ├── middleware     <- handle all fast API middleware
│    │   ├── models         <- ML, DL  LLM models
│    │   │
│    │   └── utils          <- controller and utils (useful functions)
|    |
│    └── main_script.py
|
└── docker-compose.yaml     <- to dockerize back end
---
```

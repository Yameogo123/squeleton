

Welcome to my python squeleton. This will show you how to use it directly for your projects. 

### steps:

#### 1. requirements:

- you need, of course, to install python on your computer.
- you need then to install cookiecutter `pip install cookiecutter`

#### 2. project initialization

```
cookiecutter https://github.com/Yameogo123/squeleton.git --directory="pythonPackage"
```


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
├── requirements.txt   <- The requirements file for the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── pyproject.toml     <- makes installable (pip install -e .) so src can be imported
│
├── src/{{cookiecutter.project_slug}}                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── features       <- for engineering
│   │
│   ├── data           <- Scripts for data quality
│   │
│   ├── models         <- Scripts to train models and use them for predictions
│   │
│   └── utils
│
├── tests               <- to test the functions
|
└── docker-compose.yaml         <- to dockerize front and back end
---
```

#### 4. how it works

a- Install an environment and activate it

for pyenv users:

```
make pyenv_env
```

for conda users: (you may be brought to activate your env by your own if not done)

```
make conda_env
```

b- Install required packages
(may take a while as there are many packages to install)

```
make dev-install
```

c- Check the documentation of the used functions

```
make sphinx-livehtml
```

and then open the html file in the browser: ```http://127.0.0.1:8001/```

(be free to update the documentation. Once you did it you can clean and rebuild it)
- clean it with: ```make sphinx-clean```
- and then rebuild it with: ```make sphinx-livehtml```


d- Run the basic streamlit app:

```
make run_app_front
```

e- Run the back end:

Before running it you need to create .env file in the root of the project and add variables in the .env.template file

and then

```
make run_app_back
```


<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>


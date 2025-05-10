
Squeleton usage
===============



Welcome to my python squeleton. This will show you how to use it directly for your projects. 

### steps:

1. requirements: 
----------------

- you need, of course, to install python on your computer.
  
- you need then to install cookiecutter `pip install cookiecutter`


2. project initialization
-------------------------

cookiecutter https://github.com/Yameogo123/python_squeleton.git 


3. the squeleton 
----------------


.. code-block:: markdown

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
    │   ├── etl           <- Scripts to transform data
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │
    │   ├── models         <- Scripts to train models and use them for predictions
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    ├── tests               <- to test the functions
    |
    └── docker-compose.yaml         <- to dockerize front and back end



1. how it works
---------------

a- Install an environment and activate it
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

for pyenv users:

.. code-block:: shell

    make pyenv_env


for conda users: (you may be brought to activate your env by your own if not done)

.. code-block:: shell

    make conda_env


b- Install required packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell
    
    make dev-install

c- Check the documentation of the used functions

.. code-block:: shell

    make sphinx-livehtml


and then open the html file in the browser: ``http://127.0.0.1:8001/``

(be free to update the documentation. Once you did it you can clean and rebuild it)
- clean it with: ``make sphinx-clean``
- and then rebuild it with: ``make sphinx-livehtml``



Project based on 
the "https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template


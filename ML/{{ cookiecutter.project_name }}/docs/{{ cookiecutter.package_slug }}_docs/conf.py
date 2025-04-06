

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from datetime import date

# -- Project information -----------------------------------------------------

project = f'{{ cookiecutter.project_name }}'
copyright = f'{date.today().year}, TnT'
author = f'{{ cookiecutter.project_name }}'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.graphviz",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.viewcode",
    "sphinx_git",
    "sphinx_inline_tabs",
    "sphinxcontrib.mermaid",
    "sphinx_copybutton",
    "sphinx_favicon",
    "sphinx_last_updated_by_git",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx_simplepdf",
    'sphinxcontrib.youtube',
    "sphinxcontrib.googleanalytics",    
]

# Change with your Google Analytics ID
googleanalytics_id = "G-XXXXXXXX"

# Delete Warning dupplicate label
suppress_warnings = ['autosectionlabel.*']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "*/README.rst",
    "README.rst",
    "**.ipynb_checkpoints",
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
# html_theme = 'furo'
# html_theme = 'sphinx_book_theme'
html_theme = 'furo'

html_theme_options = {
    "top_of_page_button": "edit",
    # "source_edit_link": "https://gitlab.com/keyrus-data/knowledge/knowledge-data/edit/main/{filename}",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = []
html_static_path = ['_static']

# By default, generated HTML <title> has the value project release documentation. E.g. Tech writer at work 1.0 documentation.
# If you don’t have conf.py’s release set, it is e.g., Tech writer at work  documentation (please note two spaces among “work” and “documentation”).
# If you don’t like word “documentation” or two-space issue, you have to set custom title in html_title conf.py option. For example, let’s set it to the same value as a project option.
html_title = project

# Code examples are highlighted by default syntax highlight language, if not configured otherwise for a particular example. Sphinx default syntax highlighting mode is 'python3'.
# Maybe as Sphinx is mainly used in Python projects, it is reasonable value, but I personally almost always change it to ''none'' that turns off syntax highlighting
highlight_language = 'none'


favicons = [
    {
        "href": "_static/icon.svg"
    },  # => use `_static/icon.svg`
]


html_use_index = True


# -- Options for LaTeX output --------------------------------
title = f'{{ cookiecutter.project_name }}'  # \\newline\\newline\\large PDF Version"
# The master toctree document.
master_doc = "index"
latex_theme = "manual"  # 'manual' to make a book, 'howto' to make an article
latex_documents = [("index", f"{{ cookiecutter.project_name }}.tex", title, author, "howto")]
# latex_engine = 'xelatex'
latex_logo = "./_static/logo.jpg"

latex_elements = {
    # 'papersize': 'a4paper',  # 'letterpaper' or 'a4paper'
    # 'pointsize': '10pt',     # global fontsize, possible values are 10pt, 11pt and 12pt
    # 'sphinxsetup': 'hmargin={1.5cm,1.5cm}, vmargin={2cm,2cm}',
    # 'classoptions': ',twocolumn',    # to have two columns
    "tableofcontents": "",  # To remove the TOC
    # 'babel' : '\\usepackage[english]{babel}',
}


# -- Options for simple pdf output --------------------------------
version = "1.0"

simplepdf_debug = False

simplepdf_file_name = f'{{ cookiecutter.project_name }}.pdf'

simplepdf_vars = {
    # 'cover-overlay': 'rgba(26, 150, 26, 0.7)',
    # 'primary-opaque': 'rgba(26, 150, 26, 0.7)',
    "cover-bg": "url(cover-bg.jpg) no-repeat center",
    "primary": "#28C6FF",
    "secondary": "#000000",
    "cover": "#ffffff",
    "white": "#ffffff",
    "links": "#28C6FE",
    "top-left-content": "counter(page)",
    # 'top-center-content': '',
    "top-right-content": "string(heading)",
    # 'bottom-left-content': 'counter(page)',
    "bottom-center-content": '"TnT"',
    # 'bottom-right-content': 'string(heading)',
}

import datetime
from pathlib import Path

from fyCursor import Info
self = Info()
project = "fyCursor"
author = "Baffu Team"
copyright = f"{datetime.date.today().year}, {author}"
release = self.__version__

todo_include_todos = True
pygments_style = "sphinx"
htmlhelp_basename = project
html_theme_options = {}
highlight_language = "python3"

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx-prompt",
    "sphinx_substitution_extensions",
    "sphinx_copybutton",
    "sphinxcontrib.towncrier.ext",
]

rst_prolog = f"""
.. |api_version| replace:: {self.__version__}

.. role:: pycode(code)
   :language: python3
"""

# language = None
locale_dirs = ["locale/"]
gettext_compact = False

exclude_patterns = []
source_suffix = ".rst"
master_doc = "index"

latex_documents = [
    (
        master_doc,
        f"{project}.tex",
        f"{project} Documentation",
        author,
        "manual"
    ),
]
man_pages = [(master_doc, project, f"{project} Documentation", [author], 1)]
texinfo_documents = [
    (
        master_doc,
        project,
        f"{project} Documentation",
        author,
        project,
        "Modern and fully asynchronous framework for Telegram Bot API",
        "Miscellaneous",
    ),
]

# add_module_names = False

towncrier_draft_autoversion_mode = 'draft'
towncrier_draft_include_empty = False
towncrier_draft_working_directory = Path(__file__).parent.parent

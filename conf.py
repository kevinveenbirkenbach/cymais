# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CyMaIS - Cyber Master Infrastructure Solution'
copyright = '2025, Kevin Veen-Birkenbach'
author = 'Kevin Veen-Birkenbach'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['docs', 'venv', 'venv/**']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_sidebars = {
    '**': [
        'localtoc.html',  # Zeigt die lokale Navigation an
        'relations.html',  # Vorherige/Nächste Seite
        'searchbox.html',  # Suchfeld
    ]
}

html_theme_options = {
    'fixed_sidebar': True,
}

# Liste der Dateiendungen, die Sphinx verarbeiten soll:
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "myst_parser",
]
autosummary_generate = True

# Optional: Zusätzliche MyST-Konfigurationen
myst_enable_extensions = [
    "colon_fence",  # Für erweiterte Syntax wie ::: Hinweisboxen etc.
    # weitere Erweiterungen nach Bedarf
]

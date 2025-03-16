# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

project = 'CyMaIS - Cyber Master Infrastructure Solution'
copyright = '2025, Kevin Veen-Birkenbach'
author = 'Kevin Veen-Birkenbach'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = ['docs', 'venv', 'venv/**']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinxawesome_theme'
html_static_path = ['_static']

html_sidebars = {
    '**': [
        'globaltoc.html',
        'relations.html',
        # 'sourcelink.html',
        'local_md_files.html',  # Include your custom template
        'searchbox.html',
    ]
}


html_theme_options = {
    # 'fixed_sidebar': True,
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
    'local_md_files',
    'roles_overview',
    'markdown_include',
]
autosummary_generate = True

# Optional: Zusätzliche MyST-Konfigurationen
myst_enable_extensions = [
    "colon_fence",  # Für erweiterte Syntax wie ::: Hinweisboxen etc.
    # weitere Erweiterungen nach Bedarf
]

def setup(app):
    python_domain = app.registry.domains.get('py')
    if python_domain is not None:
        directive = python_domain.directives.get('currentmodule')
        if directive is not None:
            directive.optional_arguments = 10
    return {'version': '1.0', 'parallel_read_safe': True}




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

templates_path = ['templates']
exclude_patterns = ['docs', 'venv', 'venv/**']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinxawesome_theme'
html_static_path = ['static']

html_sidebars = {
    '**': [
        #'globaltoc.html',
        # 'relations.html',
        # 'sourcelink.html',
        'structure.html',  # Include your custom template
        # 'searchbox.html',
    ]
}


html_theme_options = {
    # 'fixed_sidebar': True,
    "show_prev_next": False,
}

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

sys.path.insert(0, os.path.abspath('./extensions'))
extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.autodoc',
    'myst_parser',
    'extensions.local_file_headings',
    'extensions.local_subfolders',
    'extensions.roles_overview',
    'extensions.markdown_include',
]

autosummary_generate = True

myst_enable_extensions = [
    "colon_fence", 
]

def setup(app):
    python_domain = app.registry.domains.get('py')
    if python_domain is not None:
        directive = python_domain.directives.get('currentmodule')
        if directive is not None:
            directive.optional_arguments = 10
    return {'version': '1.0', 'parallel_read_safe': True}




import sys
import logging

# Check if a verbose flag is present in the command line arguments.
if any(arg in sys.argv for arg in ["-v", "--verbose"]):
    logging_level = logging.DEBUG
else:
    logging_level = logging.INFO

logging.basicConfig(level=logging_level)

import os
sys.path.insert(0, os.path.abspath('.'))

project = 'CyMaIS - Cyber Master Infrastructure Solution'
copyright = '2025, Kevin Veen-Birkenbach'
author = 'Kevin Veen-Birkenbach'

# -- General configuration ---------------------------------------------------
templates_path = ['templates']
exclude_patterns = ['docs', 'venv', 'venv/**']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinxawesome_theme'
html_static_path = ['static']

html_sidebars = {
    '**': [
        'structure.html',  # Include your custom template
    ]
}

html_theme_options = {
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

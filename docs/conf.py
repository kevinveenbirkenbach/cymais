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

# Highlighting for Jinja
from sphinx.highlighting import lexers
from pygments.lexers.templates import DjangoLexer

lexers['jinja'] = DjangoLexer()
lexers['j2'] = DjangoLexer()

# -- General configuration ---------------------------------------------------
templates_path = ['templates']
exclude_patterns = [
    'docs/build', 
    'venv', 
    'venv/**'
    ]

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinxawesome_theme'
html_static_path = ['assets']

html_sidebars = {
    '**': [
        'logo.html',
        'structure.html',  # Include your custom template
    ]
}

cymais_logo = "assets/img/logo.png"
html_favicon = "assets/img/favicon.ico"

html_theme_options = {
    "show_prev_next": False,
    "logo_light": cymais_logo,
    "logo_dark": cymais_logo,
}

source_suffix = {
    '.md': 'markdown',
    '.rst': 'restructuredtext',
    '.yml': 'restructuredtext',
    '.yaml': 'restructuredtext',
}

sys.path.insert(0, os.path.abspath('./extensions'))

extensions = [
    #'sphinx.ext.autosummary',
    'myst_parser',
    'extensions.local_file_headings',
    'extensions.local_subfolders',
    'extensions.roles_overview',
    'extensions.markdown_include',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

autosummary_generate = True

myst_enable_extensions = [
    "colon_fence", 
]

import logging
from docutils import nodes

logger = logging.getLogger(__name__)

def replace_assets_in_doctree(app, doctree, docname):
    # Replace asset references in image nodes
    for node in doctree.traverse(nodes.image):
        if "assets/" in node['uri']:
            new_uri = node['uri'].replace("assets/", "_static/")
            node['uri'] = new_uri
            logger.info("Replaced image URI in {}: {}".format(docname, new_uri))
    
    # Replace asset references in raw HTML nodes
    for node in doctree.traverse(nodes.raw):
        if node.get('format') == 'html' and "assets/" in node.astext():
            new_text = node.astext().replace("assets/", "_static/")
            node.children = [nodes.raw('', new_text, format='html')]
            logger.info("Replaced raw HTML assets in {}.".format(docname))

def setup(app):
    app.connect("doctree-resolved", replace_assets_in_doctree)
    
    python_domain = app.registry.domains.get('py')
    if python_domain is not None:
        directive = python_domain.directives.get('currentmodule')
        if directive is not None:
            directive.optional_arguments = 10
    return {'version': '1.0', 'parallel_read_safe': True}

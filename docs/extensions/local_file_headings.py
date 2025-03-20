import os
import sys
import logging as std_logging  # Use the standard logging module
from sphinx.util import logging  # Sphinx logging is used elsewhere if needed
from docutils.parsers.rst import Directive
from .nav_utils import natural_sort_key, extract_headings_from_file, group_headings, sort_tree, MAX_HEADING_LEVEL, DEFAULT_MAX_NAV_DEPTH

# Set up our logger based on command-line args.
logger = std_logging.getLogger(__name__)
if any(arg in sys.argv for arg in ["-v", "--verbose"]):
    logger.setLevel(std_logging.DEBUG)
else:
    logger.setLevel(std_logging.INFO)

DEFAULT_MAX_NAV_DEPTH = 4

def add_local_file_headings(app, pagename, templatename, context, doctree):
    logger.debug("add_local_file_headings called with pagename: %s", pagename)
    
    srcdir = app.srcdir
    directory = os.path.dirname(pagename)
    abs_dir = os.path.join(srcdir, directory)
    if not os.path.isdir(abs_dir):
        logger.warning("Directory %s not found for page %s.", abs_dir, pagename)
        context['local_md_headings'] = []
        return

    # Get only files with .md or .rst extensions.
    files = [f for f in os.listdir(abs_dir) if f.endswith('.md') or f.endswith('.rst')]
    # If an index file is present, remove any readme files (case-insensitive).
    files_lower = [f.lower() for f in files]
    if 'index.rst' in files_lower:
        files = [f for f in files if f.lower() not in ['readme.md']]

    file_items = []
    for file in files:
        filepath = os.path.join(abs_dir, file)
        headings = extract_headings_from_file(filepath, max_level=MAX_HEADING_LEVEL)
        basename, _ = os.path.splitext(file)
        # Set priority: index gets priority 0, otherwise 1.
        priority = 0 if basename.lower() == 'index' else 1
        for heading in headings:
            file_link = os.path.join(directory, basename)
            file_items.append({
                'level': heading['level'],
                'text': heading['text'],
                'link': file_link,
                'anchor': heading['anchor'],
                'priority': priority,
                'filename': basename
            })
    tree = group_headings(file_items)
    sort_tree(tree)

    logger.debug("Generated tree: %s", tree)
    context['local_md_headings'] = tree

def setup(app):
    app.add_config_value('local_nav_max_depth', DEFAULT_MAX_NAV_DEPTH, 'env')
    app.connect('html-page-context', add_local_file_headings)
    return {'version': '0.1', 'parallel_read_safe': True}

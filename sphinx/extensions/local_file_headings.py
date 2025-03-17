import os
import sys
import logging as std_logging  # Use the standard logging module
from sphinx.util import logging  # Sphinx logging is used elsewhere if needed
from docutils.parsers.rst import Directive
from .nav_utils import natural_sort_key, extract_headings_from_file, group_headings, sort_tree, MAX_HEADING_LEVEL, DEFAULT_MAX_NAV_DEPTH

# Use standard logging to set the level based on command-line args.
logger = std_logging.getLogger(__name__)
if any(arg in sys.argv for arg in ["-v", "--verbose"]):
    logger.setLevel(std_logging.DEBUG)
else:
    logger.setLevel(std_logging.INFO)

DEFAULT_MAX_NAV_DEPTH = 4

def postprocess_current(nodes, current_file, current_anchor):
    """
    Recursively process the tree nodes in post-order.
    If a node or any child node matches the current file and anchor,
    mark that node as current.
    Returns True if the current subtree contains a current node.
    """
    found_in_subtree = False
    for node in nodes:
        # Process children first (post-order)
        child_found = False
        if 'children' in node and node['children']:
            child_found = postprocess_current(node['children'], current_file, current_anchor)
        
        # Get the file and anchor for the current node, trimming trailing slashes and whitespace.
        node_file = node.get('link', '').rstrip('/')
        node_anchor = node.get('anchor', '').strip()
        
        # Debug: output the current node's values and the comparison values.
        logger.debug("Checking node: text=%s, link=%s, anchor=%s", 
                     node.get('text', ''),
                     node_file,
                     node_anchor)
        logger.debug("Comparing with current_file=%s, current_anchor=%s", 
                     current_file.rstrip('/'),
                     current_anchor.strip())
        
        # Mark node as current if it exactly matches the current file and anchor.
        if node_file == current_file.rstrip('/') and node_anchor == current_anchor.strip():
            node['current'] = True
            logger.debug("Node '%s' marked as current (exact match).", node.get('text', ''))
            found = True
        else:
            node['current'] = child_found
            if child_found:
                logger.debug("Node '%s' marked as current (child match).", node.get('text', ''))
        
        if node['current']:
            found_in_subtree = True
    return found_in_subtree

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
    if 'index.md' in files_lower or 'index.rst' in files_lower:
        files = [f for f in files if f.lower() not in ['readme.md', 'readme.rst']]

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

    # Determine current file and anchor.
    # This implementation assumes that if an anchor is present, it is appended to pagename as "#anchor".
    if '#' in pagename:
        current_file, current_anchor = pagename.split('#', 1)
    else:
        current_file, current_anchor = pagename, ''
    
    logger.debug("Current file: %s, Current anchor: %s", current_file, current_anchor)

    # Postprocess the tree: bubble up the 'current' flag from children to parents.
    if current_anchor:
        postprocess_current(tree, current_file, current_anchor)
    else:
        logger.debug("No anchor provided; skipping current marking.")

    logger.debug("Final tree after postprocessing: %s", tree)
    context['local_md_headings'] = tree

def setup(app):
    app.add_config_value('local_nav_max_depth', DEFAULT_MAX_NAV_DEPTH, 'env')
    app.connect('html-page-context', add_local_file_headings)
    return {'version': '0.1', 'parallel_read_safe': True}

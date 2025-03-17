import os
import re
from sphinx.util import logging
from docutils.parsers.rst import Directive
from .nav_utils import natural_sort_key, extract_headings_from_file, group_headings, sort_tree, MAX_HEADING_LEVEL, DEFAULT_MAX_NAV_DEPTH

logger = logging.getLogger(__name__)

def collect_subfolder_tree(dir_path, base_url, current_depth, max_depth):
    """
    Recursively collects navigation items from subdirectories.
    For each subfolder, it looks for a candidate file (prefer "index.rst" then "README.md")
    and extracts its first level‑1 heading as the title. If no candidate or heading is found,
    the folder name is used.
    Returns a list representing the subfolder tree.
    """
    items = []
    for item in sorted(os.listdir(dir_path), key=lambda s: s.lower()):
        full_path = os.path.join(dir_path, item)
        if os.path.isdir(full_path):
            candidate = None
            for cand in ['index.rst', 'README.md']:
                candidate_path = os.path.join(full_path, cand)
                if os.path.isfile(candidate_path):
                    candidate = candidate_path
                    break
            if candidate:
                headings = extract_headings_from_file(candidate, max_level=MAX_HEADING_LEVEL)
                title = headings[0]['text'] if headings else item
            else:
                title = item
            link = os.path.join(base_url, item)
            entry = {
                'level': 1,
                'text': title,
                'link': link,
                'anchor': '',
                'priority': 0,
                'filename': item
            }
            if current_depth < max_depth:
                children = collect_subfolder_tree(full_path, os.path.join(base_url, item), current_depth + 1, max_depth)
                if children:
                    entry['children'] = children
            items.append(entry)
    return items

def add_local_subfolders(app, pagename, templatename, context, doctree):
    """
    Collects a tree of subfolder navigation items from the current directory.
    For each subfolder, the title is determined by scanning for a candidate file (prefer "index.rst" then "README.md")
    and extracting its first level‑1 heading, or using the folder name if none is found.
    The resulting tree is stored in context['local_subfolders'].
    """
    srcdir = app.srcdir
    directory = os.path.dirname(pagename)
    abs_dir = os.path.join(srcdir, directory)
    if not os.path.isdir(abs_dir):
        logger.warning(f"Directory {abs_dir} not found for page {pagename}.")
        context['local_subfolders'] = []
        return

    max_nav_depth = getattr(app.config, 'local_nav_max_depth', DEFAULT_MAX_NAV_DEPTH)
    subfolder_tree = collect_subfolder_tree(abs_dir, directory, current_depth=0, max_depth=max_nav_depth)
    sort_tree(subfolder_tree)
    context['local_subfolders'] = subfolder_tree

def setup(app):
    # Do not add the config value here to avoid conflicts.
    app.connect('html-page-context', add_local_subfolders)
    return {'version': '0.1', 'parallel_read_safe': True}

import os
from sphinx.util import logging
from .nav_utils import extract_headings_from_file, MAX_HEADING_LEVEL

logger = logging.getLogger(__name__)

CANDIDATES = ['index.rst', 'readme.md', 'main.rst']

def collect_folder_tree(dir_path, base_url):
    """
    Recursively collects the folder tree starting from the given directory.

    For each folder:
    - Hidden folders (names starting with a dot) are skipped.
    - A folder is processed only if it contains one of the representative files:
      index.rst, index.md, readme.md, or readme.rst.
    - The first heading of the representative file is used as the folder title.
    - The representative file is not listed as a file in the folder.
    - All other Markdown and reStructuredText files are listed without sub-headings,
      using their first heading as the file title.
    """
    # Skip hidden directories
    if os.path.basename(dir_path).startswith('.'):
        return None

    # List all files in the current directory with .md or .rst extension
    files = [f for f in os.listdir(dir_path)
             if os.path.isfile(os.path.join(dir_path, f))
             and (f.endswith('.md') or f.endswith('.rst'))]

    # Find representative file for folder title using index or readme
    rep_file = None
    for candidate in CANDIDATES:
        for f in files:
            if f.lower() == candidate:
                rep_file = f
                break
        if rep_file:
            break

    # Skip this folder if no representative file exists
    if not rep_file:
        return None

    rep_path = os.path.join(dir_path, rep_file)
    headings = extract_headings_from_file(rep_path, max_level=MAX_HEADING_LEVEL)
    folder_title = headings[0]['text'] if headings else os.path.basename(dir_path)
    folder_link = os.path.join(base_url, os.path.splitext(rep_file)[0])

    # Remove the representative file from the list to avoid duplication,
    # and filter out any additional "readme.md" or "index.rst" files.
    files.remove(rep_file)
    files = [f for f in files if f.lower() not in CANDIDATES]

    # Process the remaining files in the current directory
    file_items = []
    for file in sorted(files, key=lambda s: s.lower()):
        file_path = os.path.join(dir_path, file)
        file_headings = extract_headings_from_file(file_path, max_level=MAX_HEADING_LEVEL)
        file_title = file_headings[0]['text'] if file_headings else file
        file_base = os.path.splitext(file)[0]
        file_link = os.path.join(base_url, file_base)
        file_items.append({
            'level': 1,
            'text': file_title,
            'link': file_link,
            'anchor': '',
            'priority': 1,
            'filename': file
        })

    # Process subdirectories (ignoring hidden ones)
    dir_items = []
    for item in sorted(os.listdir(dir_path), key=lambda s: s.lower()):
        full_path = os.path.join(dir_path, item)
        if os.path.isdir(full_path) and not item.startswith('.'):
            subtree = collect_folder_tree(full_path, os.path.join(base_url, item))
            if subtree:
                dir_items.append(subtree)

    # Combine files and subdirectories as children of the current folder
    children = file_items + dir_items

    return {
        'text': folder_title,
        'link': folder_link,
        'children': children,
        'filename': os.path.basename(dir_path)
    }

def mark_current(node, active):
    """
    Recursively mark nodes as current if the active page (pagename)
    matches the node's link or is a descendant of it.

    The function sets node['current'] = True if:
    - The node's link matches the active page exactly, or
    - The active page begins with the node's link plus a separator (indicating a child).
    Additionally, if any child node is current, the parent is marked as current.
    """
    is_current = False
    node_link = node.get('link', '').rstrip('/')
    active = active.rstrip('/')
    if node_link and (active == node_link or active.startswith(node_link + '/')):
        is_current = True

    # Recurse into children if they exist
    children = node.get('children', [])
    for child in children:
        if mark_current(child, active):
            is_current = True

    node['current'] = is_current
    return is_current

def add_local_subfolders(app, pagename, templatename, context, doctree):
    """
    Sets the 'local_subfolders' context variable with the entire folder tree
    starting from app.srcdir, and marks the tree with the 'current' flag up
    to the active page.
    """
    root_dir = app.srcdir
    folder_tree = collect_folder_tree(root_dir, '')
    if folder_tree:
        mark_current(folder_tree, pagename)
    context['local_subfolders'] = [folder_tree] if folder_tree else []

def setup(app):
    app.connect('html-page-context', add_local_subfolders)
    return {'version': '0.1', 'parallel_read_safe': True}

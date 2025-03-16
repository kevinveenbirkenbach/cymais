import os
import re
from sphinx.util import logging

logger = logging.getLogger(__name__)

# Set the maximum heading level for Markdown headings
MAX_HEADING_LEVEL = 3
DEFAULT_MAX_NAV_DEPTH = 2  # Default maximum navigation depth; configurable via conf.py

def natural_sort_key(text):
    """
    Generate a key for natural (human-friendly) sorting,
    where numbers in the text are taken into account by their numeric value.
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split('(\d+)', text)]

def extract_headings_from_file(filepath, max_level=MAX_HEADING_LEVEL):
    """
    Extract headings from a file.
    For Markdown files, look for lines starting with '#' (up to max_level).
    For reStructuredText files, look for a line immediately followed by an underline made of punctuation.
    """
    headings = []
    ext = os.path.splitext(filepath)[1].lower()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            if ext == '.md':
                in_code_block = False
                for line in f:
                    if line.strip().startswith("```"):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block:
                        continue
                    match = re.match(r'^(#{1,})\s+(.*)$', line)
                    if match:
                        level = len(match.group(1))
                        if level <= max_level:
                            heading_text = match.group(2).strip()
                            anchor = re.sub(r'\s+', '-', heading_text.lower())
                            anchor = re.sub(r'[^a-z0-9\-]', '', anchor)
                            headings.append({'level': level, 'text': heading_text, 'anchor': anchor})
            elif ext == '.rst':
                lines = f.readlines()
                for i in range(len(lines)-1):
                    text_line = lines[i].rstrip("\n")
                    underline = lines[i+1].rstrip("\n")
                    if len(underline) >= 3 and re.fullmatch(r'[-=~\^\+"\'`]+', underline):
                        level = 1  # default level; adjust if needed
                        heading_text = text_line.strip()
                        anchor = re.sub(r'\s+', '-', heading_text.lower())
                        anchor = re.sub(r'[^a-z0-9\-]', '', anchor)
                        headings.append({'level': level, 'text': heading_text, 'anchor': anchor})
    except Exception as e:
        logger.warning(f"Error reading {filepath}: {e}")
    return headings

def group_headings(headings):
    """
    Converts a flat list of headings into a tree structure based on their level.
    Each heading gets a 'children' list.
    """
    tree = []
    stack = []
    for heading in headings:
        heading['children'] = []
        while stack and stack[-1]['level'] >= heading['level']:
            stack.pop()
        if stack:
            stack[-1]['children'].append(heading)
        else:
            tree.append(heading)
        stack.append(heading)
    return tree

def sort_tree(tree):
    """
    Sorts a list of headings (and their children) first by their 'priority' (default 1)
    and then by the natural sort key of their text.
    """
    tree.sort(key=lambda x: (x.get('priority', 1), natural_sort_key(x['text'])))

def collect_nav_items(dir_path, base_url, current_depth, max_depth):
    """
    Recursively collects navigation items from subdirectories.
    For each subdirectory, if an 'index.rst' exists (preferred) or a 'readme.md' exists,
    the first heading from that file is used as the title.
    """
    nav_items = []
    # Look for candidate file in this subdirectory (prefer index.rst, then readme.md)
    candidate = None
    for cand in ['index.rst', 'readme.md']:
        candidate_path = os.path.join(dir_path, cand)
        if os.path.isfile(candidate_path):
            candidate = cand
            break
    if candidate:
        candidate_path = os.path.join(dir_path, candidate)
        headings = extract_headings_from_file(candidate_path)
        if headings:
            title = headings[0]['text']
        else:
            title = os.path.splitext(candidate)[0].capitalize()
        # Build link relative to base_url
        link = os.path.join(base_url, os.path.splitext(candidate)[0])
        nav_items.append({
            'level': 1,
            'text': title,
            'link': link,
            'anchor': '',
            'priority': 0
        })
    # Recurse into subdirectories if within max_depth
    if current_depth < max_depth:
        for item in os.listdir(dir_path):
            full_path = os.path.join(dir_path, item)
            if os.path.isdir(full_path):
                sub_base_url = os.path.join(base_url, item)
                nav_items.extend(collect_nav_items(full_path, sub_base_url, current_depth + 1, max_depth))
    return nav_items

def add_local_md_headings(app, pagename, templatename, context, doctree):
    srcdir = app.srcdir
    directory = os.path.dirname(pagename)
    abs_dir = os.path.join(srcdir, directory)
    if not os.path.isdir(abs_dir):
        logger.warning(f"Directory {abs_dir} not found for page {pagename}.")
        context['local_md_headings'] = []
        return

    max_nav_depth = getattr(app.config, 'local_nav_max_depth', DEFAULT_MAX_NAV_DEPTH)

    # Collect navigation items from subdirectories only
    nav_items = []
    for item in os.listdir(abs_dir):
        full_path = os.path.join(abs_dir, item)
        if os.path.isdir(full_path):
            nav_items.extend(collect_nav_items(full_path, os.path.join(directory, item), current_depth=1, max_depth=max_nav_depth))

    # Process files in the current directory.
    files = os.listdir(abs_dir)
    files_lower = [f.lower() for f in files]
    # If both index.rst and readme.md exist in the current directory, keep only index.rst.
    if "index.rst" in files_lower:
        files = [f for f in files if f.lower() != "readme.md"]
    local_md_headings = []
    for file in files:
        if file.endswith('.md') or file.endswith('.rst'):
            filepath = os.path.join(abs_dir, file)
            headings = extract_headings_from_file(filepath)
            basename, _ = os.path.splitext(file)
            # Set priority: index/readme files get priority 0.
            if basename.lower() in ['index', 'readme']:
                priority = 0
            else:
                priority = 1
            for heading in headings:
                file_link = os.path.join(directory, basename)
                local_md_headings.append({
                    'level': heading['level'],
                    'text': heading['text'],
                    'link': file_link,
                    'anchor': heading['anchor'],
                    'priority': priority
                })
    # Combine current directory items with subdirectory nav items.
    # If an index or readme from the current directory exists, it will be included only once.
    all_items = local_md_headings + nav_items
    tree = group_headings(all_items)
    sort_tree(tree)
    context['local_md_headings'] = tree

def setup(app):
    app.add_config_value('local_nav_max_depth', DEFAULT_MAX_NAV_DEPTH, 'env')
    app.connect('html-page-context', add_local_md_headings)
    return {'version': '0.1', 'parallel_read_safe': True}

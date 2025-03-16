import os
import re
from sphinx.util import logging

logger = logging.getLogger(__name__)

# Set the maximum heading level to include (e.g., include headings up to H3)
MAX_HEADING_LEVEL = 3

def natural_sort_key(text):
    """
    Generate a key for natural (human-friendly) sorting,
    where numbers in the text are taken into account by their numeric value.
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split('(\d+)', text)]

def extract_headings_from_file(filepath, max_level=MAX_HEADING_LEVEL):
    """
    Extract Markdown headings (up to max_level) from the file at filepath.
    Skips fenced code blocks.
    """
    headings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            in_code_block = False
            for line in f:
                # Toggle code block state if a line starts with ```
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue
                # Match Markdown headings: one or more '#' followed by a space and the title.
                match = re.match(r'^(#{1,})\s+(.*)$', line)
                if match:
                    level = len(match.group(1))
                    if level <= max_level:
                        heading_text = match.group(2).strip()
                        # Create a simple slug for the anchor:
                        # - convert to lowercase
                        # - replace spaces with hyphens
                        # - remove non-alphanumeric characters (except hyphens)
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
        # Pop headings from the stack that are at or deeper than the current level
        while stack and stack[-1]['level'] >= heading['level']:
            stack.pop()
        if stack:
            # Append the current heading as a child of the last item in the stack
            stack[-1]['children'].append(heading)
        else:
            tree.append(heading)
        stack.append(heading)
    return tree

def sort_tree(tree):
    """
    Sorts a list of headings (and their children) by their text.
    """
    tree.sort(key=lambda x: natural_sort_key(x['text']))
    for node in tree:
        if node.get('children'):
            sort_tree(node['children'])

def add_local_md_headings(app, pagename, templatename, context, doctree):
    srcdir = app.srcdir
    directory = os.path.dirname(pagename)
    abs_dir = os.path.join(srcdir, directory)
    if not os.path.isdir(abs_dir):
        logger.warning(f"Directory {abs_dir} not found for page {pagename}.")
        context['local_md_headings'] = []
        return

    local_md_headings = []
    for file in os.listdir(abs_dir):
        if file.endswith('.md'):
            filepath = os.path.join(abs_dir, file)
            headings = extract_headings_from_file(filepath)
            for heading in headings:
                base = file[:-3]
                file_link = os.path.join(directory, base)
                local_md_headings.append({
                    'level': heading['level'],
                    'text': heading['text'],
                    'link': file_link,
                    'anchor': heading['anchor']
                })
    # Proceed with grouping and sorting as before...
    tree = group_headings(local_md_headings)
    sort_tree(tree)
    context['local_md_headings'] = tree

def setup(app):
    app.connect('html-page-context', add_local_md_headings)
    return {'version': '0.1', 'parallel_read_safe': True}

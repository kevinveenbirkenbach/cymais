import os
import re
from sphinx.util import logging

logger = logging.getLogger(__name__)

# Set the maximum heading level to include (e.g., include headings up to H3 for Markdown)
MAX_HEADING_LEVEL = 3

def natural_sort_key(text):
    """
    Generate a key for natural (human-friendly) sorting,
    where numbers in the text are taken into account by their numeric value.
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split('(\d+)', text)]

def extract_headings_from_file(filepath, max_level=MAX_HEADING_LEVEL):
    """
    Extract headings from a file. For Markdown files, look for lines starting with '#' (up to max_level).
    For reStructuredText files, look for a line that is immediately followed by an underline made of punctuation.
    """
    headings = []
    ext = os.path.splitext(filepath)[1].lower()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            if ext == '.md':
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
                            anchor = re.sub(r'\s+', '-', heading_text.lower())
                            anchor = re.sub(r'[^a-z0-9\-]', '', anchor)
                            headings.append({'level': level, 'text': heading_text, 'anchor': anchor})
            elif ext == '.rst':
                lines = f.readlines()
                # Look for reST headings: a line followed by an underline made of punctuation.
                for i in range(len(lines)-1):
                    text_line = lines[i].rstrip("\n")
                    underline = lines[i+1].rstrip("\n")
                    if len(underline) >= 3 and re.fullmatch(r'[-=~\^\+"\'`]+', underline):
                        level = 1  # default level; you could adjust based on the punctuation if needed
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
    Sorts a list of headings (and their children) first by their 'priority' (if defined, default 1)
    and then by the natural sort key of their text.
    """
    tree.sort(key=lambda x: (x.get('priority', 1), natural_sort_key(x['text'])))

def add_local_md_headings(app, pagename, templatename, context, doctree):
    srcdir = app.srcdir
    directory = os.path.dirname(pagename)
    abs_dir = os.path.join(srcdir, directory)
    if not os.path.isdir(abs_dir):
        logger.warning(f"Directory {abs_dir} not found for page {pagename}.")
        context['local_md_headings'] = []
        return

    # List all files in the directory.
    files = os.listdir(abs_dir)
    files_lower = [f.lower() for f in files]
    # If both index.rst and README.md exist, filter out README.md (case-insensitive)
    if "index.rst" in files_lower:
        files = [f for f in files if f.lower() != "readme.md"]

    local_md_headings = []
    for file in files:
        if file.endswith('.md') or file.endswith('.rst'):
            filepath = os.path.join(abs_dir, file)
            headings = extract_headings_from_file(filepath)
            # Determine file priority: index and readme get priority 0; others 1.
            basename, _ = os.path.splitext(file)
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
    tree = group_headings(local_md_headings)
    sort_tree(tree)
    context['local_md_headings'] = tree

def setup(app):
    app.connect('html-page-context', add_local_md_headings)
    return {'version': '0.1', 'parallel_read_safe': True}

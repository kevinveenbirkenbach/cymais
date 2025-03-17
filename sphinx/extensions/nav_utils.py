import os
import re
import yaml

DEFAULT_MAX_NAV_DEPTH = 4
MAX_HEADING_LEVEL = 2

def natural_sort_key(text):
    """
    Generate a key for natural (human-friendly) sorting,
    taking numeric parts into account.
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

def extract_headings_from_file(filepath, max_level=MAX_HEADING_LEVEL):
    """
    Extract headings from a file.
    For Markdown (.md) files, looks for lines starting with '#' (up to max_level).
    For reStructuredText (.rst) files, looks for a line immediately followed by an underline.
    Returns a list of dictionaries with keys: 'level', 'text', and 'anchor' (if applicable).
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
                        level = 1
                        heading_text = text_line.strip()
                        # For reST, the anchor is left empty (can be generated later if needed)
                        headings.append({'level': level, 'text': heading_text, 'anchor': ''})
    except Exception as e:
        print(f"Warning: Error reading {filepath}: {e}")
    return headings

def group_headings(headings):
    """
    Convert a flat list of headings into a tree structure based on their level.
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
    Sort a tree of navigation items, first by a 'priority' value (lower comes first)
    and then by a natural sort key based on the 'filename' field (or the 'text' field if no filename is provided).
    This ensures that 'index' and 'readme' (priority 0) always appear at the top.
    """
    tree.sort(key=lambda x: (x.get('priority', 1), natural_sort_key(x.get('filename', x['text']))))
    for item in tree:
        if item.get('children'):
            sort_tree(item['children'])


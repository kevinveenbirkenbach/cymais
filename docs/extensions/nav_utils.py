import os
import re
import yaml

DEFAULT_MAX_NAV_DEPTH = 4
MAX_HEADING_LEVEL = 0  # This can be overridden in your configuration

def natural_sort_key(text):
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

def extract_headings_from_file(filepath, max_level=MAX_HEADING_LEVEL):
    # If max_level is 0, set it to a very high value to effectively iterate infinitely
    if max_level == 0:
        max_level = 9999

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
                    # Assuming markdown headings are defined with '#' characters
                    match = re.match(r'^(#{1,})(.*?)$', line)
                    if match:
                        level = len(match.group(1))
                        if level <= max_level:
                            heading_text = match.group(2).strip()
                            anchor = re.sub(r'\s+', '-', heading_text.lower())
                            anchor = re.sub(r'[^a-z0-9\-]', '', anchor)
                            headings.append({'level': level, 'text': heading_text, 'anchor': anchor})
            elif ext == '.rst':
                lines = f.readlines()
                for i in range(len(lines) - 1):
                    text_line = lines[i].rstrip("\n")
                    underline = lines[i+1].rstrip("\n")
                    if len(underline) >= 3 and re.fullmatch(r'[-=~\^\+"\'`]+', underline):
                        level = 1
                        heading_text = text_line.strip()
                        headings.append({'level': level, 'text': heading_text, 'anchor': ''})
    except Exception as e:
        print(f"Warning: Error reading {filepath}: {e}")
    if not headings:
        base = os.path.basename(filepath).lower()
        if base == 'index.rst':
            folder = os.path.dirname(filepath)
            readme_path = os.path.join(folder, 'README.md')
            if os.path.isfile(readme_path):
                try:
                    headings = extract_headings_from_file(readme_path, max_level)
                except Exception as e:
                    print(f"Warning: Error reading fallback README.md in {folder}: {e}")
    return headings

def group_headings(headings):
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
    tree.sort(key=lambda x: (x.get('priority', 1), natural_sort_key(x.get('filename', x['text']))))
    for item in tree:
        if item.get('children'):
            sort_tree(item['children'])

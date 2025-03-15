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

def add_local_md_headings(app, pagename, templatename, context, doctree):
    """
    For every Markdown file in the same directory as the current page,
    extract its headings, sort them in natural ascending order, and add them
    to the context.
    """
    srcdir = app.srcdir
    # Determine the directory of the current page (e.g., "directory/file" -> "directory")
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
                file_link = os.path.join(directory, file) if directory else file
                full_link = file_link + '#' + heading['anchor']
                local_md_headings.append({
                    'level': heading['level'],
                    'text': heading['text'],
                    'link': full_link
                })
    # Sort headings in natural ascending order using natural_sort_key.
    local_md_headings.sort(key=lambda x: natural_sort_key(x['text']))
    context['local_md_headings'] = local_md_headings

def setup(app):
    app.connect('html-page-context', add_local_md_headings)
    return {'version': '0.1', 'parallel_read_safe': True}

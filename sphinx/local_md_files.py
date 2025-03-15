import os
from sphinx.util import logging

logger = logging.getLogger(__name__)

def add_local_md_files(app, pagename, templatename, context, doctree):
    srcdir = app.srcdir
    # Determine the directory of the current page (e.g., "directory/file" → "directory")
    directory = os.path.dirname(pagename)
    abs_dir = os.path.join(srcdir, directory)
    if not os.path.isdir(abs_dir):
        logger.warning(f"Directory {abs_dir} not found for page {pagename}.")
        context['local_md_files'] = []
        return

    md_files = []
    for file in os.listdir(abs_dir):
        if file.endswith('.md'):
            # Optionally: Skip the current file in the list
            if file == os.path.basename(pagename):
                continue
            # Create a link relative to the source directory
            link = os.path.join(directory, file) if directory else file
            md_files.append({'name': file, 'link': link})
    context['local_md_files'] = md_files

def setup(app):
    # Connect the handler to the "html-page-context" event
    app.connect('html-page-context', add_local_md_files)
    return {'version': '0.1', 'parallel_read_safe': True}

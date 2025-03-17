import os
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util import logging

logger = logging.getLogger(__name__)

from myst_parser.parsers.sphinx_ import MystParser

class MarkdownIncludeDirective(Directive):
    required_arguments = 1  # Path to the Markdown file
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False

    def run(self):
        logger.info("Executing markdown-include directive")
        env = self.state.document.settings.env
        # Determine the absolute path of the file.
        rel_filename, filename = env.relfn2path(self.arguments[0])
        logger.info("Markdown file: %s", filename)
        if not os.path.exists(filename):
            error = self.state_machine.reporter.error(
                f'File not found: {filename}',
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
        except Exception as e:
            error = self.state_machine.reporter.error(
                f'Error reading file {filename}: {e}',
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return [error]

        # Parse the Markdown content with MystParser.
        parser = MystParser()
        from docutils.frontend import OptionParser
        from docutils.utils import new_document
        settings = OptionParser(components=(MystParser,)).get_default_values()
        # Attach the Sphinx environment to the settings so that myst_parser works.
        settings.env = self.state.document.settings.env
        doc = new_document(filename, settings=settings)
        parser.parse(markdown_content, doc)
        logger.info("Markdown parsing completed successfully")

        # Remove the first header (title) if it exists.
        if doc.children:
            first_section = doc.children[0]
            if isinstance(first_section, nodes.section) and first_section.children:
                first_child = first_section.children[0]
                if isinstance(first_child, nodes.title):
                    # If there are additional children, remove the title node.
                    if len(first_section.children) > 1:
                        first_section.pop(0)
                        logger.info("Removed first header from Markdown content")
                    else:
                        # If it's the only child, clear its content instead.
                        first_child.clear()
                        logger.info("Cleared text of first header from Markdown content")
            
            # Unwrap the first section if it no longer has a title.
            if isinstance(first_section, nodes.section):
                has_title = any(isinstance(child, nodes.title) and child.astext().strip() 
                                for child in first_section.children)
                if not has_title:
                    # Remove the section wrapper so that its content does not create a TOC entry.
                    unwrapped = list(first_section.children)
                    # Replace the first section with its children.
                    doc.children = unwrapped + doc.children[1:]
                    logger.info("Unwrapped first section to avoid a TOC entry")

        return doc.children

def setup(app):
    app.add_directive("markdown-include", MarkdownIncludeDirective)
    return {'version': '0.1', 'parallel_read_safe': True}

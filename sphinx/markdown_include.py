import os
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util import logging

logger = logging.getLogger(__name__)

from myst_parser.parsers.sphinx_ import MystParser

class MarkdownIncludeDirective(Directive):
    required_arguments = 1  # Pfad zur Markdown-Datei
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False

    def run(self):
        logger.info("markdown-include-Direktive wird ausgeführt")
        env = self.state.document.settings.env
        # Ermittle den absoluten Pfad der Datei.
        rel_filename, filename = env.relfn2path(self.arguments[0])
        logger.info("Markdown-Datei: %s", filename)
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

        # Parse den Markdown-Content mit MystParser.
        parser = MystParser()
        from docutils.frontend import OptionParser
        from docutils.utils import new_document
        settings = OptionParser(components=(MystParser,)).get_default_values()
        # Hänge die Sphinx-Umgebung an die Einstellungen an, damit myst_parser funktioniert.
        settings.env = self.state.document.settings.env
        doc = new_document(filename, settings=settings)
        parser.parse(markdown_content, doc)
        logger.info("Markdown-Parsing erfolgreich abgeschlossen")
        return doc.children

def setup(app):
    app.add_directive("markdown-include", MarkdownIncludeDirective)
    return {'version': '0.1', 'parallel_read_safe': True}

import os
import glob
import yaml
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList
from sphinx.util import logging

logger = logging.getLogger(__name__)

class RolesOverviewDirective(Directive):
    """
    A directive to embed a roles overview as reStructuredText.
    
    It scans the roles directory (i.e. every folder under "roles") for a
    "meta/main.yml" file, reads the category (if provided) and the role’s description
    (from galaxy_info.description), and outputs a listing grouped by category.
    """
    has_content = False

    def run(self):
        env = self.state.document.settings.env
        srcdir = env.srcdir
        roles_dir = os.path.join(srcdir, 'roles')
        if not os.path.isdir(roles_dir):
            logger.warning(f"Roles directory not found: {roles_dir}")
            error_node = self.state.document.reporter.error(
                "Roles directory not found.", line=self.lineno)
            return [error_node]

        # Dictionary mapping categories to role entries.
        categories = {}
        for role_path in glob.glob(os.path.join(roles_dir, '*')):
            if os.path.isdir(role_path):
                meta_path = os.path.join(role_path, 'meta', 'main.yml')
                if os.path.exists(meta_path):
                    try:
                        with open(meta_path, 'r', encoding='utf-8') as f:
                            data = yaml.safe_load(f)
                    except Exception as e:
                        logger.warning(f"Error reading YAML file {meta_path}: {e}")
                        continue

                    role_name = os.path.basename(role_path)
                    category = data.get('category', 'uncategorized')
                    role_description = data.get('galaxy_info', {}).get('description', '')
                    role_entry = {
                        'name': role_name,
                        'description': role_description,
                        'link': f'roles/{role_name}/README.md'
                    }
                    categories.setdefault(category, []).append(role_entry)
                else:
                    logger.warning(f"meta/main.yml not found for role {role_path}")

        # Sort categories and roles alphabetically.
        sorted_categories = sorted(categories.items(), key=lambda x: x[0].lower())
        for category, roles in sorted_categories:
            roles.sort(key=lambda r: r['name'].lower())

        # Build reStructuredText content.
        lines = []
        for category, roles in sorted_categories:
            lines.append(f".. rubric:: {category}")
            lines.append("")
            for role in roles:
                lines.append(f"* **[`{role['name']}`]({role['link']})**")
                if role['description']:
                    lines.append(f"  - {role['description']}")
            lines.append("")

        rst_content = "\n".join(lines)

        # Use a ViewList for nested_parse.
        rst_lines = ViewList()
        for i, line in enumerate(rst_content.splitlines()):
            rst_lines.append(line, '<roles-overview>')

        container = nodes.container()
        self.state.nested_parse(rst_lines, self.content_offset, container)
        return [container]

def setup(app):
    app.add_directive("roles-overview", RolesOverviewDirective)
    return {'version': '0.1', 'parallel_read_safe': True}

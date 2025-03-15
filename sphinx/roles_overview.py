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
    "meta/main.yml" file, reads the role’s galaxy tags (from galaxy_info.galaxy_tags)
    and description (from galaxy_info.description), and outputs a listing grouped
    by each tag. Roles without galaxy tags are grouped under "uncategorized".
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

        # Dictionary mapping tags to role entries.
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
                    # Try to get galaxy_tags from galaxy_info. If none, use "uncategorized".
                    galaxy_info = data.get('galaxy_info', {})
                    tags = galaxy_info.get('galaxy_tags', [])
                    if not tags:
                        tags = ['uncategorized']
                    role_description = galaxy_info.get('description', '')
                    role_entry = {
                        'name': role_name,
                        'description': role_description,
                        'link': f'roles/{role_name}/README.md',
                        'tags': tags,
                    }
                    # Add this role to every tag it belongs to.
                    for tag in tags:
                        categories.setdefault(tag, []).append(role_entry)
                else:
                    logger.warning(f"meta/main.yml not found for role {role_path}")

        # Sort categories and roles alphabetically.
        sorted_categories = sorted(categories.items(), key=lambda x: x[0].lower())
        for tag, roles in sorted_categories:
            roles.sort(key=lambda r: r['name'].lower())

        # Build reStructuredText content.
        lines = []
        for tag, roles in sorted_categories:
            lines.append(f".. rubric:: {tag}")
            lines.append("")
            for role in roles:
                # Render the role name as a hyperlink in reStructuredText.
                lines.append(f"* `{role['name']} <{role['link']}>`_")
                # Insert a line break before the description.
                if role['description']:
                    lines.append("")
                    lines.append(f"  {role['description']}")
                lines.append("")
            lines.append("")

        rst_content = "\n".join(lines)

        # Use a ViewList for nested_parse.
        rst_lines = ViewList()
        for line in rst_content.splitlines():
            rst_lines.append(line, '<roles-overview>')

        container = nodes.container()
        self.state.nested_parse(rst_lines, self.content_offset, container)
        return [container]

def setup(app):
    app.add_directive("roles-overview", RolesOverviewDirective)
    return {'version': '0.1', 'parallel_read_safe': True}

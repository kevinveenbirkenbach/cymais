import os
import glob
import re
import yaml
from docutils import nodes
from sphinx.util import logging
from docutils.parsers.rst import Directive

logger = logging.getLogger(__name__)

class RolesOverviewDirective(Directive):
    """
    A directive to embed a roles overview as reStructuredText.

    It scans the roles directory (each folder under "roles") for a "meta/main.yml" file,
    reads the role’s galaxy tags and description, and outputs an overview grouped by tag.
    For each role, it attempts to extract a level‑1 heading from its README.md as the title.
    If no title is found, the role folder name is used.
    The title is rendered as a clickable link to the role's README.md.
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

        # Gather role entries grouped by tag.
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
                    # Determine title from README.md if available.
                    readme_path = os.path.join(role_path, 'README.md')
                    title = role_name
                    if os.path.exists(readme_path):
                        try:
                            with open(readme_path, 'r', encoding='utf-8') as f:
                                for line in f:
                                    match = re.match(r'^#\s+(.*)$', line)
                                    if match:
                                        title = match.group(1).strip()
                                        break
                        except Exception as e:
                            logger.warning(f"Error reading README.md for {role_name}: {e}")

                    galaxy_info = data.get('galaxy_info', {})
                    tags = galaxy_info.get('galaxy_tags', [])
                    if not tags:
                        tags = ['uncategorized']
                    role_description = galaxy_info.get('description', '')
                    role_entry = {
                        'name': role_name,
                        'title': title,
                        'description': role_description,
                        'link': f'roles/{role_name}/README.md',
                        'tags': tags,
                    }
                    for tag in tags:
                        categories.setdefault(tag, []).append(role_entry)
                else:
                    logger.warning(f"meta/main.yml not found for role {role_path}")

        # Sort categories and roles alphabetically.
        sorted_categories = sorted(categories.items(), key=lambda x: x[0].lower())
        for tag, roles in sorted_categories:
            roles.sort(key=lambda r: r['name'].lower())

        # Build the document structure.
        container = nodes.container()

        # For each category add a rubric heading.
        for tag, roles in sorted_categories:
            rubric = nodes.rubric(text=tag)
            container += rubric

            # For each role create a separate section.
            for role in roles:
                # Create a section with an explicit ID.
                section_id = nodes.make_id(role['title'])
                section = nodes.section(ids=[section_id])
                # Create a title node that contains a reference.
                title_node = nodes.title()
                reference = nodes.reference(text=role['title'], refuri=role['link'])
                title_node += reference
                section += title_node

                if role['description']:
                    para = nodes.paragraph(text=role['description'])
                    section += para

                container += section

        return [container]

def setup(app):
    app.add_directive("roles-overview", RolesOverviewDirective)
    return {'version': '0.1', 'parallel_read_safe': True}

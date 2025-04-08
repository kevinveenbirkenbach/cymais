from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import glob
import os
import re
import yaml

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        """
        This lookup iterates over all roles whose folder name starts with 'docker-'
        and generates a list of dictionaries (cards). For each role, it:
          - Extracts the application_id (everything after "docker-")
          - Reads the title from the role's README.md (the first H1 line)
          - Retrieves the description from galaxy_info.description in meta/main.yml
          - Retrieves the icon class from galaxy_info.logo.class
          - Builds the URL using the 'domains' variable (e.g. domains[application_id])
          - Sets the iframe flag from applications[application_id].landingpage_iframe_enabled

        Only cards whose application_id is included in the variable group_names are returned.
        """
        # Default to "roles" if no directory is provided
        roles_dir = terms[0] if len(terms) > 0 else "roles"
        cards = []

        # Get group_names from variables; default to empty list if not set
        group_names = variables.get("group_names", [])

        # Pattern to match roles starting with "docker-"
        pattern = os.path.join(roles_dir, "docker-*")
        for role_path in glob.glob(pattern):
            role_dir = role_path.rstrip("/")
            role_basename = os.path.basename(role_dir)
            if not role_basename.startswith("docker-"):
                continue

            # The application_id is the substring after "docker-"
            application_id = role_basename[len("docker-"):]

            # Only add card if the application_id is in group_names
            if application_id not in group_names:
                continue

            # Define paths for the README.md and meta/main.yml
            readme_path = os.path.join(role_dir, "README.md")
            meta_path = os.path.join(role_dir, "meta", "main.yml")
            if not os.path.exists(readme_path) or not os.path.exists(meta_path):
                continue

            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    readme_content = f.read()
                # Extract the first H1 line (title) via regex
                title_match = re.search(r'^#\s+(.*)$', readme_content, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else application_id
            except Exception as e:
                raise AnsibleError("Error reading '{}': {}".format(readme_path, str(e)))

            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta_data = yaml.safe_load(f)
                galaxy_info = meta_data.get("galaxy_info", {})
                description = galaxy_info.get("description", "")
                logo = galaxy_info.get("logo", {})
                icon_class = logo.get("class", "fa-solid fa-cube")
            except Exception as e:
                raise AnsibleError("Error reading '{}': {}".format(meta_path, str(e)))

            # Retrieve variables for domain and application settings.
            domains = variables.get("domains", {})
            applications = variables.get("applications", {})
            domain_url = domains.get(application_id, "")
            url = "https://" + domain_url if domain_url else ""
            app_data = applications.get(application_id, {})
            iframe = app_data.get("landingpage_iframe_enabled", False)

            card = {
                "icon": {"class": icon_class},
                "title": title,
                "text": description,
                "url": url,
                "link_text": "Discover {} Now!".format(title),
                "iframe": iframe,
            }
            cards.append(card)
        return [cards]

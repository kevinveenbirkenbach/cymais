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
          - Retrieves the tags from galaxy_info.galaxy_tags
          - Builds the URL using the 'domains' variable (e.g. domains | get_domain(application_id))
          - Sets the iframe flag from applications[application_id].features.iframe

        Only cards whose application_id is included in the variable group_names are returned.
        """
        # Default to "roles" directory if no path is provided
        roles_dir = terms[0] if len(terms) > 0 else "roles"
        cards = []

        # Retrieve group_names from variables (used to filter roles)
        group_names = variables.get("group_names", [])

        # Search for all roles starting with "docker-"
        pattern = os.path.join(roles_dir, "docker-*")
        for role_path in glob.glob(pattern):
            role_dir = role_path.rstrip("/")
            role_basename = os.path.basename(role_dir)

            # Skip roles not starting with "docker-"
            if not role_basename.startswith("docker-"):
                continue

            # Extract application_id from role name
            application_id = role_basename[len("docker-"):]

            # Skip roles not listed in group_names
            if application_id not in group_names:
                continue

            # Define paths to README.md and meta/main.yml
            readme_path = os.path.join(role_dir, "README.md")
            meta_path = os.path.join(role_dir, "meta", "main.yml")

            # Skip role if required files are missing
            if not os.path.exists(readme_path) or not os.path.exists(meta_path):
                continue

            # Extract title from first H1 line in README.md
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    readme_content = f.read()
                title_match = re.search(r'^#\s+(.*)$', readme_content, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else application_id
            except Exception as e:
                raise AnsibleError("Error reading '{}': {}".format(readme_path, str(e)))

            # Extract metadata from meta/main.yml
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta_data = yaml.safe_load(f)

                galaxy_info = meta_data.get("galaxy_info", {})
                
                # If display is set to False ignore it
                if not galaxy_info.get("display", True):
                    continue
                
                description = galaxy_info.get("description", "")
                logo = galaxy_info.get("logo", {})
                icon_class = logo.get("class", "fa-solid fa-cube")
                tags = galaxy_info.get("galaxy_tags", [])
            except Exception as e:
                raise AnsibleError("Error reading '{}': {}".format(meta_path, str(e)))

            # Retrieve domains and applications from the variables
            domains = variables.get("domains", {})
            applications = variables.get("applications", {})
            domain_url = domains.get(application_id, "")

            if isinstance(domain_url, list):
                domain_url = domain_url[0]
            elif isinstance(domain_url, dict):
                domain_url = next(iter(domain_url.values()))
                
            # Construct the URL using the domain_url if available.
            url = "https://" + domain_url if domain_url else ""

            app_data = applications.get(application_id, {})
            iframe = app_data.get("features", {}).get("portfolio_iframe", False)

            # Build card dictionary
            card = {
                "icon": {"class": icon_class},
                "title": title,
                "text": description,
                "url": url,
                "link_text": "Discover {} Now!".format(title),
                "iframe": iframe,
                "tags": tags,
            }

            cards.append(card)

        # Sort A-Z
        cards.sort(key=lambda c: c['title'].lower())

        # Return the list of cards
        return [cards]

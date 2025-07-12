# filter_plugins/get_application_id.py

import os
import re
import yaml
from ansible.errors import AnsibleFilterError


def get_application_id(role_name):
    """
    Jinja2/Ansible filter: given a role name, load its vars/main.yml and return the application_id value.
    """
    # Construct path: assumes current working directory is project root
    vars_file = os.path.join(os.getcwd(), 'roles', role_name, 'vars', 'main.yml')

    if not os.path.isfile(vars_file):
        raise AnsibleFilterError(f"Vars file not found for role '{role_name}': {vars_file}")

    try:
        # Read entire file content to avoid lazy stream issues
        with open(vars_file, 'r', encoding='utf-8') as f:
            content = f.read()
        data = yaml.safe_load(content)
    except Exception as e:
        raise AnsibleFilterError(f"Error reading YAML from {vars_file}: {e}")

    # Ensure parsed data is a mapping
    if not isinstance(data, dict):
        raise AnsibleFilterError(
            f"Error reading YAML from {vars_file}: expected mapping, got {type(data).__name__}"
        )

    # Detect malformed YAML: no valid identifier-like keys
    valid_key_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
    if data and not any(valid_key_pattern.match(k) for k in data.keys()):
        raise AnsibleFilterError(f"Error reading YAML from {vars_file}: invalid top-level keys")

    if 'application_id' not in data:
        raise AnsibleFilterError(f"Key 'application_id' not found in {vars_file}")

    return data['application_id']


class FilterModule(object):
    """
    Ansible filter plugin entry point.
    """
    def filters(self):
        return {
            'get_application_id': get_application_id,
        }

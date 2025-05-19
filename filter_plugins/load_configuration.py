import os
import yaml
import re
from ansible.errors import AnsibleFilterError

# in-memory cache: application_id → (parsed_yaml, is_nested)
_cfg_cache = {}

def load_configuration(application_id, key):
    if not isinstance(key, str):
        raise AnsibleFilterError("Key must be a dotted-string, e.g. 'features.matomo'")

    # locate roles/
    here = os.path.dirname(__file__)
    root = os.path.abspath(os.path.join(here, '..'))
    roles_dir = os.path.join(root, 'roles')
    if not os.path.isdir(roles_dir):
        raise AnsibleFilterError(f"Roles directory not found at {roles_dir}")

    # first time? load & cache
    if application_id not in _cfg_cache:
        config_path = None

        # 1) primary: vars/main.yml declares it
        for role in os.listdir(roles_dir):
            mv = os.path.join(roles_dir, role, 'vars', 'main.yml')
            if os.path.exists(mv):
                try:
                    md = yaml.safe_load(open(mv)) or {}
                except Exception:
                    md = {}
                if md.get('application_id') == application_id:
                    cf = os.path.join(roles_dir, role, 'vars', 'configuration.yml')
                    if not os.path.exists(cf):
                        raise AnsibleFilterError(
                            f"Role '{role}' declares '{application_id}' but missing configuration.yml"
                        )
                    config_path = cf
                    break

        # 2) fallback nested
        if config_path is None:
            for role in os.listdir(roles_dir):
                cf = os.path.join(roles_dir, role, 'vars', 'configuration.yml')
                if not os.path.exists(cf):
                    continue
                try:
                    dd = yaml.safe_load(open(cf)) or {}
                except Exception:
                    dd = {}
                if isinstance(dd, dict) and application_id in dd:
                    config_path = cf
                    break

        # 3) fallback flat
        if config_path is None:
            for role in os.listdir(roles_dir):
                cf = os.path.join(roles_dir, role, 'vars', 'configuration.yml')
                if not os.path.exists(cf):
                    continue
                try:
                    dd = yaml.safe_load(open(cf)) or {}
                except Exception:
                    dd = {}
                # flat style: dict with all non-dict values
                if isinstance(dd, dict) and not any(isinstance(v, dict) for v in dd.values()):
                    config_path = cf
                    break

        if config_path is None:
            return None

        # parse once
        try:
            parsed = yaml.safe_load(open(config_path)) or {}
        except Exception as e:
            raise AnsibleFilterError(f"Error loading configuration.yml at {config_path}: {e}")

        # detect nested vs flat
        is_nested = isinstance(parsed, dict) and (application_id in parsed)
        _cfg_cache[application_id] = (parsed, is_nested)

    parsed, is_nested = _cfg_cache[application_id]

    # pick base entry
    entry = parsed[application_id] if is_nested else parsed

    # resolve dotted key
    key_parts = key.split('.')
    for part in key_parts:
        # Check if part has an index (e.g., domains.canonical[0])
        match = re.match(r'([^\[]+)\[([0-9]+)\]', part)
        if match:
            part, index = match.groups()
            index = int(index)
            if isinstance(entry, dict) and part in entry:
                entry = entry[part]
                # Check if entry is a list and access the index
                if isinstance(entry, list) and 0 <= index < len(entry):
                    entry = entry[index]
                else:
                    raise AnsibleFilterError(
                        f"Index '{index}' out of range for key '{part}' in application '{application_id}'"
                    )
            else:
                raise AnsibleFilterError(
                    f"Key '{part}' not found under application '{application_id}'"
                )
        else:
            if isinstance(entry, dict) and part in entry:
                entry = entry[part]
            else:
                raise AnsibleFilterError(
                    f"Key '{part}' not found under application '{application_id}'"
                )

    return entry


class FilterModule(object):
    def filters(self):
        return {'load_configuration': load_configuration}

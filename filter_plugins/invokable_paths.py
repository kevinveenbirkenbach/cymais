import os
import yaml
from typing import Dict, List, Optional


def get_invokable_paths(
    roles_file: Optional[str] = None,
    suffix: Optional[str] = None
) -> List[str]:
    """
    Load nested roles YAML from the given file (or default at project root) and return
    dash-joined paths where 'invokable' is True. Appends suffix if provided.

    :param roles_file: Optional path to YAML file. Defaults to '<project_root>/roles/categories.yml'.
    :param suffix: Optional suffix to append to each invokable path.
    :return: List of invokable paths.
    :raises FileNotFoundError: If the YAML file cannot be found.
    :raises yaml.YAMLError: If the YAML file cannot be parsed.
    :raises ValueError: If the root of the YAML is not a dictionary.
    """
    # Determine default roles_file if not provided
    if not roles_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        roles_file = os.path.join(project_root, 'roles', 'categories.yml')

    # Load and validate YAML
    try:
        with open(roles_file, 'r') as f:
            data = yaml.safe_load(f) or {}
    except FileNotFoundError:
        raise FileNotFoundError(f"Roles file not found: {roles_file}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML {roles_file}: {e}")

    if not isinstance(data, dict):
        raise ValueError("YAML root is not a dictionary")

    # Unwrap if single 'roles' key
    roles = data
    if 'roles' in roles and isinstance(roles['roles'], dict) and len(roles) == 1:
        roles = roles['roles']

    def _recurse(subroles: Dict[str, dict], parent: List[str] = None) -> List[str]:
        parent = parent or []
        found: List[str] = []
        METADATA = {'title', 'description', 'icon', 'invokable'}

        for key, cfg in subroles.items():
            path = parent + [key]
            if cfg.get('invokable', False):
                p = '-'.join(path)
                if suffix:
                    p += suffix
                found.append(p)

            # Recurse into non-metadata child dicts
            children = {
                ck: cv for ck, cv in cfg.items()
                if ck not in METADATA and isinstance(cv, dict)
            }
            if children:
                found.extend(_recurse(children, path))
        return found

    return _recurse(roles)


class FilterModule:
    def filters(self):
        return {'invokable_paths': get_invokable_paths}

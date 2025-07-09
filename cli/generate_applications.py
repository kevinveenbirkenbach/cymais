#!/usr/bin/env python3

import argparse
import os
import yaml
import sys
from pathlib import Path

plugin_path = Path(__file__).resolve().parent / ".." / "lookup_plugins"
sys.path.insert(0, str(plugin_path))

from application_gid import LookupModule

def load_yaml_file(path):
    """Load a YAML file if it exists, otherwise return an empty dict."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main():
    parser = argparse.ArgumentParser(
        description="Generate defaults_applications YAML from docker roles and include users meta data for each role."
    )
    parser.add_argument(
        "--roles-dir",
        help="Path to the roles directory (default: roles)"
    )
    parser.add_argument(
        "--output-file",
        help="Path to output YAML file"
    )

    args = parser.parse_args()
    cwd = Path.cwd()
    roles_dir = (cwd / args.roles_dir).resolve()
    output_file = (cwd / args.output_file).resolve()
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Initialize result structure
    result = {"defaults_applications": {}}

    gid_lookup = LookupModule()
    # Process each role for application configs
    for role_dir in sorted(roles_dir.iterdir()):
        role_name = role_dir.name
        vars_main = role_dir / "vars" / "main.yml"
        config_file = role_dir / "config" / "main.yml"

        if not vars_main.exists():
            print(f"[!] Skipping {role_name}: vars/main.yml missing")
            continue

        vars_data = load_yaml_file(vars_main)
        try:
            application_id = vars_data.get("application_id")
        except Exception as e:
            print(
                f"Warning: failed to read application_id from {vars_main}\nException: {e}",
                file=sys.stderr
            )
            sys.exit(1)

        if not application_id:
            print(f"[!] Skipping {role_name}: application_id not defined in vars/main.yml")
            continue

        if not config_file.exists():
            print(f"[!] Skipping {role_name}: config/main.yml missing")
            continue

        config_data = load_yaml_file(config_file)
        if config_data:
            try:
                gid_number = gid_lookup.run([application_id], roles_dir=str(roles_dir))[0]
            except Exception as e:
                print(f"Warning: failed to determine gid for '{application_id}': {e}", file=sys.stderr)
                sys.exit(1)
            config_data["group_id"] = gid_number
            result["defaults_applications"][application_id] = config_data
            users_meta_file = role_dir / "users" / "main.yml"
            transformed_users = {}
            if users_meta_file.exists():
                users_meta = load_yaml_file(users_meta_file)
                users_data = users_meta.get("users", {})
                for user, role_user_attrs in users_data.items():
                    transformed_users[user] = f"{{{{ users[\"{user}\"] }}}}"

            # Attach transformed users under each application
            if transformed_users:
                result["defaults_applications"][application_id]["users"] = transformed_users

    # Write out result YAML
    with output_file.open("w", encoding="utf-8") as f:
        yaml.dump(result, f, sort_keys=False)

    try:
        print(f"✅ Generated: {output_file.relative_to(cwd)}")
    except ValueError:
        print(f"✅ Generated: {output_file}")


if __name__ == "__main__":
    main()

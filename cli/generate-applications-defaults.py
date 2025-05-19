#!/usr/bin/env python3

import argparse
import os
import yaml
import sys
from pathlib import Path

def load_yaml_file(path):
    """Load a YAML file if it exists, otherwise return an empty dict."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def main():
    parser = argparse.ArgumentParser(description="Generate defaults_applications YAML from docker roles.")
    parser.add_argument("--roles-dir", default="roles", help="Path to the roles directory (default: roles)")
    parser.add_argument("--output-file", default="group_vars/all/03_applications.yml", help="Path to output YAML file")

    args = parser.parse_args()
    cwd = Path.cwd()
    roles_dir = (cwd / args.roles_dir).resolve()
    output_file = (cwd / args.output_file).resolve()

    output_file.parent.mkdir(parents=True, exist_ok=True)

    result = {"defaults_applications": {}}

    for role_dir in sorted(roles_dir.iterdir()):
        role_name = role_dir.name
        vars_main = role_dir / "vars" / "main.yml"
        config_file = role_dir / "vars" / "configuration.yml"

        if not vars_main.exists():
            print(f"[!] Skipping {role_name}: vars/main.yml missing")
            continue

        vars_data = load_yaml_file(vars_main)
        try:
            application_id = vars_data.get("application_id")
        except Exception as e:
            # print the exception message
            print(f"Warning: failed to read application_id from {vars_data} in {vars_main}.\nException: {e}", file=sys.stderr)
            # exit with status 0
            sys.exit(1)

        if not application_id:
            print(f"[!] Skipping {role_name}: application_id not defined in vars/main.yml")
            continue

        if not config_file.exists():
            print(f"[!] Skipping {role_name}: vars/configuration.yml missing")
            continue

        config_data = load_yaml_file(config_file)
        if config_data:
            result["defaults_applications"][application_id] = config_data

    with output_file.open("w", encoding="utf-8") as f:
        yaml.dump(result, f, sort_keys=False)

    try:
        print(f"✅ Generated: {output_file.relative_to(cwd)}")
    except ValueError:
        print(f"✅ Generated: {output_file}")

if __name__ == "__main__":
    main()

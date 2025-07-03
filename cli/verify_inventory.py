#!/usr/bin/env python3
import argparse
import sys
import yaml
import re
from pathlib import Path


def load_yaml_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            content = re.sub(r'(?m)^([ \t]*[^\s:]+):\s*!vault[\s\S]+?(?=^\S|\Z)', r'\1: "<vaulted>"\n', content)
            return yaml.safe_load(content)
    except Exception as e:
        print(f"Warning: Could not parse {path}: {e}", file=sys.stderr)
        return None


def recursive_keys(d, prefix=""):
    keys = set()
    if isinstance(d, dict):
        for k, v in d.items():
            full_key = f"{prefix}.{k}" if prefix else k
            keys.add(full_key)
            keys.update(recursive_keys(v, full_key))
    return keys


def compare_application_keys(applications, defaults, source_file):
    errors = []
    for app_id, app_conf in applications.items():
        if app_id not in defaults:
            errors.append(f"{source_file}: Unknown application '{app_id}' (not in defaults_applications)")
            continue

        default_conf = defaults.get(app_id, {})
        app_keys = recursive_keys(app_conf)
        default_keys = recursive_keys(default_conf)

        for key in app_keys:
            if key.startswith("credentials."):
                continue  # explicitly ignore credentials
            if key not in default_keys:
                errors.append(f"{source_file}: Missing default for {app_id}: {key}")
    return errors


def load_inventory_files(inventory_dir):
    all_data = {}
    inventory_path = Path(inventory_dir)

    for path in inventory_path.glob("*.yml"):
        data = load_yaml_file(path)
        if isinstance(data, dict):
            applications = data.get("applications") or data.get("defaults_applications")
            if applications:
                all_data[path] = applications

    for vars_folder in inventory_path.glob("*_vars"):
        if vars_folder.is_dir():
            for subfile in vars_folder.rglob("*.yml"):
                data = load_yaml_file(subfile)
                if isinstance(data, dict):
                    applications = data.get("applications") or data.get("defaults_applications")
                    if applications:
                        all_data[subfile] = applications

    return all_data


def find_defaults_applications_file():
    candidates = list(Path("group_vars/all").glob("*_applications.yml"))
    if len(candidates) != 1:
        raise RuntimeError(f"Expected exactly one *_applications.yml file in group_vars/all, found {len(candidates)}")
    return candidates[0]


def main():
    parser = argparse.ArgumentParser(description="Verify application variable consistency with defaults.")
    parser.add_argument("inventory_dir", help="Path to inventory directory (contains inventory.yml and *_vars/)")
    args = parser.parse_args()

    defaults_path = find_defaults_applications_file()
    defaults_data = load_yaml_file(defaults_path)
    defaults = defaults_data.get("defaults_applications", {}) if defaults_data else {}

    if not defaults:
        print(f"Error: No 'defaults_applications' found in {defaults_path}.", file=sys.stderr)
        sys.exit(1)

    all_errors = []
    inventory_files = load_inventory_files(args.inventory_dir)
    for source_path, app_data in inventory_files.items():
        errors = compare_application_keys(app_data, defaults, str(source_path))
        all_errors.extend(errors)

    if all_errors:
        print("Validation failed with the following issues:")
        for err in all_errors:
            print("-", err)
        sys.exit(1)
    else:
        print("Inventory directory is valid against defaults.")
        sys.exit(0)


if __name__ == "__main__":
    main()

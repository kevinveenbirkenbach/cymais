#!/usr/bin/env python3
import argparse
import glob
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML is required. Install with `pip install pyyaml`.\n")
    sys.exit(1)


def find_application_ids():
    """
    Searches all files matching roles/*/vars/main.yml for the key 'application_id'
    and returns a list of all found IDs.
    """
    pattern = os.path.join('roles', '*', 'vars', 'main.yml')
    app_ids = []

    for filepath in glob.glob(pattern):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            sys.stderr.write(f"Error reading {filepath}: {e}\n")
            continue

        if isinstance(data, dict) and 'application_id' in data:
            app_ids.append(data['application_id'])

    return sorted(set(app_ids))


def main():
    parser = argparse.ArgumentParser(
        description='Output a list of all application_id values defined in roles/*/vars/main.yml'
    )
    # No arguments other than --help
    parser.parse_args()

    ids = find_application_ids()
    for app_id in ids:
        print(app_id)


if __name__ == '__main__':
    main()

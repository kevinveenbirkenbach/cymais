#!/usr/bin/env python3
"""
CLI for extracting invokable role paths from a nested roles YAML file using argparse.
Assumes a default roles file at the project root if none is provided.
"""

import os
import sys

# ─── Determine project root ───
if "__file__" in globals():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
else:
    project_root = os.getcwd()

# Ensure project root on PYTHONPATH so 'filter_plugins' can be imported
sys.path.insert(0, project_root)

import argparse
import yaml
from filter_plugins.invokable_paths import get_invokable_paths


def main():
    parser = argparse.ArgumentParser(
        description="Extract invokable role paths from a nested roles YAML file."
    )
    parser.add_argument(
        "roles_file",
        nargs='?',
        default=None,
        help="Path to the roles YAML file (default: roles/categories.yml at project root)"
    )
    parser.add_argument(
        "--suffix", "-s",
        help="Optional suffix to append to each invokable path.",
        default=None
    )
    args = parser.parse_args()

    try:
        paths = get_invokable_paths(args.roles_file, args.suffix)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    for p in paths:
        print(p)


if __name__ == "__main__":
    main()
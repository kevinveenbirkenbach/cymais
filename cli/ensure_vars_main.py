#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Generate (or preview) missing vars/main.yml for all roles with a given prefix"
    )
    parser.add_argument(
        "--prefix",
        required=True,
        help="Role-name prefix to scan for (e.g. 'desk-')"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="If set, only show what would be done without making changes"
    )
    args = parser.parse_args()
    prefix = args.prefix
    preview = args.preview

    # Locate roles/ directory relative to this script
    script_dir = Path(__file__).resolve().parent
    roles_dir = (script_dir / "../roles").resolve()

    if not roles_dir.is_dir():
        print(f"Error: roles directory not found at {roles_dir}")
        return

    missing = []
    for role in sorted(roles_dir.iterdir()):
        if not role.is_dir():
            continue
        if not role.name.startswith(prefix):
            continue

        vars_dir = role / "vars"
        vars_main = vars_dir / "main.yml"
        if not vars_main.exists():
            missing.append((role.name, vars_main))

    if not missing:
        print(f"No missing vars/main.yml files found for prefix '{prefix}'")
        return

    for role_name, vars_main in missing:
        app_id = role_name[len(prefix):]
        content = f"application_id: \"{app_id}\"\n"

        if preview:
            print(f"Would create: {vars_main}")
            print(f"With content:\n{content}")
        else:
            # ensure directory exists
            vars_main.parent.mkdir(parents=True, exist_ok=True)
            # write file
            with open(vars_main, "w") as f:
                f.write(content)
            print(f"Created {vars_main}")

if __name__ == "__main__":
    main()

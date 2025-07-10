#!/usr/bin/env python3
"""
Script to ensure each Ansible role under ../roles/ with a given prefix has a vars/main.yml
containing the correct application_id. Can preview actions or overwrite mismatches.
"""
import argparse
import sys
import yaml
from pathlib import Path

def process_role(role_dir: Path, prefix: str, preview: bool, overwrite: bool):
    name = role_dir.name
    if not name.startswith(prefix):
        return
    # Expected application_id is role name minus prefix
    expected_id = name[len(prefix):]
    vars_dir = role_dir / "vars"
    vars_file = vars_dir / "main.yml"
    if vars_file.exists():
        # Load existing variables
        try:
            existing = yaml.safe_load(vars_file.read_text()) or {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {vars_file}: {e}", file=sys.stderr)
            return
        actual_id = existing.get("application_id")
        if actual_id == expected_id:
            # Already correct
            return
        if overwrite:
            # Update only application_id
            existing["application_id"] = expected_id
            if preview:
                print(f"[PREVIEW] Would update {vars_file}: application_id -> {expected_id}")
            else:
                with open(vars_file, "w") as f:
                    yaml.safe_dump(existing, f, default_flow_style=False, sort_keys=False)
                print(f"Updated {vars_file}: application_id -> {expected_id}")
        else:
            print(f"Mismatch in {vars_file}: application_id='{actual_id}', expected='{expected_id}'")
    else:
        # Create new vars/main.yml
        if preview:
            print(f"[PREVIEW] Would create {vars_file} with application_id: {expected_id}")
        else:
            vars_dir.mkdir(parents=True, exist_ok=True)
            content = {"application_id": expected_id}
            with open(vars_file, "w") as f:
                yaml.safe_dump(content, f, default_flow_style=False, sort_keys=False)
            print(f"Created {vars_file} with application_id: {expected_id}")


def main():
    parser = argparse.ArgumentParser(
        description="Ensure vars/main.yml for roles with a given prefix has correct application_id"
    )
    parser.add_argument(
        "--prefix", required=True,
        help="Role name prefix to filter (e.g. 'web-', 'svc-', 'desk-')"
    )
    parser.add_argument(
        "--preview", action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="If vars/main.yml exists but application_id mismatches, overwrite only that key"
    )
    args = parser.parse_args()

    # Determine roles directory relative to this script
    script_dir = Path(__file__).resolve().parent
    roles_dir = (script_dir.parent / "../roles").resolve()
    if not roles_dir.is_dir():
        print(f"Roles directory not found: {roles_dir}", file=sys.stderr)
        sys.exit(1)

    for role in sorted(roles_dir.iterdir()):
        if role.is_dir():
            process_role(role, args.prefix, args.preview, args.overwrite)

if __name__ == "__main__":
    main()

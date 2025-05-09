#!/usr/bin/env python3

import os
from pathlib import Path

ROLES_DIR = Path("roles")  # Adjust this if needed
FILES_FIXED = []

def fix_tabs_in_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    if any('\t' in line for line in lines):
        fixed_lines = [line.replace('\t', '  ') for line in lines]
        with open(file_path, "w") as f:
            f.writelines(fixed_lines)
        FILES_FIXED.append(str(file_path))

def main():
    for role_dir in sorted(ROLES_DIR.iterdir()):
        if not role_dir.is_dir():
            continue

        vars_main = role_dir / "vars" / "main.yml"
        if vars_main.exists():
            fix_tabs_in_file(vars_main)

    if FILES_FIXED:
        print("✅ Fixed tab characters in the following files:")
        for f in FILES_FIXED:
            print(f"  - {f}")
    else:
        print("✅ No tabs found in any vars/main.yml files.")

if __name__ == "__main__":
    main()

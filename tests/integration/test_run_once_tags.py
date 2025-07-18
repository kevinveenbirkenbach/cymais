import os
import re
import unittest
from collections import defaultdict

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
ROLES_DIR = os.path.join(PROJECT_ROOT, 'roles')
ROOT_TASKS_DIR = os.path.join(PROJECT_ROOT, 'tasks')

def is_under_root_tasks(fpath):
    abs_path = os.path.abspath(fpath)
    return abs_path.startswith(os.path.abspath(ROOT_TASKS_DIR) + os.sep)

def find_role_includes(roles_dir):
    """
    Yields (filepath, line_number, role_name) for each import_role/include_role usage in roles/,
    but ignores anything under the root-level tasks/ dir.
    """
    for dirpath, _, filenames in os.walk(roles_dir):
        for fname in filenames:
            if not fname.endswith(('.yml', '.yaml')):
                continue
            fpath = os.path.join(dirpath, fname)
            if is_under_root_tasks(fpath):
                continue  # Skip root-level tasks dir completely
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except Exception:
                continue  # Ignore unreadable files
            for idx, line in enumerate(lines):
                if 'import_role' in line or 'include_role' in line:
                    block = line + ''.join(lines[idx+1:idx+5])
                    match = re.search(r'name:\s*[\'"]?([\w\-]+)[\'"]?', block)
                    if match:
                        role_name = match.group(1)
                        yield fpath, idx + 1, role_name

def check_run_once_tag(content, role_name):
    """
    Checks for run_once_{role_name} or # run_once_{role_name}: deactivated in content.
    """
    pattern = (
        rf'(run_once_{role_name.replace("-", "_")})'
        rf'|(#\s*run_once_{role_name.replace("-", "_")}: deactivated)'
    )
    return re.search(pattern, content, re.IGNORECASE)

class TestRunOnceTag(unittest.TestCase):
    def test_all_roles_have_run_once_tag(self):
        role_to_locations = defaultdict(list)
        role_to_first_missing = {}

        # Collect all places where roles are included/imported
        for fpath, line, role_name in find_role_includes(ROLES_DIR):
            key = role_name.replace("-", "_")
            role_to_locations[key].append((fpath, line, role_name))

        # Now check only ONCE per role if the tag exists somewhere (the first location), and record missing
        errors = {}
        for key, usages in role_to_locations.items():
            # Just pick the first usage for checking
            fpath, line, role_name = usages[0]
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                continue
            if not check_run_once_tag(content, role_name):
                error_msg = (
                    f'Role "{role_name}" is imported/included but no "run_once_{key}" tag or deactivation comment found.\n'
                    f'First found at: {fpath}, line {line}\n'
                    f'  → Add a line "run_once_{key}" to this file to prevent double execution.\n'
                    f'  → To deliberately disable this warning for this role, add:\n'
                    f'      # run_once_{key}: deactivated\n'
                    f'All occurrences:\n' +
                    ''.join([f'  - {fp}, line {ln}\n' for fp, ln, _ in usages])
                )
                errors[key] = error_msg

        if errors:
            msg = (
                "Some included/imported roles in 'roles/' are missing a run_once tag or deactivation comment:\n\n"
                + "\n".join(errors.values())
            )
            self.fail(msg)

if __name__ == '__main__':
    unittest.main()

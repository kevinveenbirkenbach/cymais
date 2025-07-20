import os
import re
import unittest
from collections import defaultdict

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')
)
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
    key = role_name.replace('-', '_')
    pattern = (
        rf'(run_once_{key})'
        rf'|(#\s*run_once_{key}: deactivated)'
    )
    return re.search(pattern, content, re.IGNORECASE)


class TestRunOnceTag(unittest.TestCase):
    def test_all_roles_have_run_once_tag(self):
        role_to_locations = defaultdict(list)

        # Collect all places where roles are included/imported
        for fpath, line, role_name in find_role_includes(ROLES_DIR):
            key = role_name.replace('-', '_')
            role_to_locations[key].append((fpath, line, role_name))

        errors = {}
        for key, usages in role_to_locations.items():
            # Only check the role's own tasks/main.yml instead of the includer file
            _, line, role_name = usages[0]
            role_tasks = os.path.join(
                ROLES_DIR, role_name, 'tasks', 'main.yml'
            )
            try:
                with open(role_tasks, 'r', encoding='utf-8') as f:
                    content = f.read()
            except FileNotFoundError:
                # Fallback to the includer file if tasks/main.yml doesn't exist
                includer_file = usages[0][0]
                with open(includer_file, 'r', encoding='utf-8') as f:
                    content = f.read()

            if not check_run_once_tag(content, role_name):
                error_msg = (
                    f'Role "{role_name}" is imported/included but no "run_once_{key}" tag or deactivation comment found.\n'
                    f'First usage at includer: {usages[0][0]}, line {line}\n'
                    f'  → Ensure "run_once_{key}" is defined in {role_tasks} or deactivate with comment.\n'
                    f'  → For example, add "# run_once_{key}: deactivated" at the top of {role_tasks} to suppress this warning.\n'
                    f'All occurrences:\n' +
                    ''.join([f'  - {fp}, line {ln}\n' for fp, ln, _ in usages])
                )
                errors[key] = error_msg

        if errors:
            msg = (
                "Some included/imported roles are missing a run_once tag or deactivation comment:\n\n"
                + "\n".join(errors.values())
            )
            self.fail(msg)


if __name__ == '__main__':
    unittest.main()

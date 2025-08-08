import os
import glob
import re
import unittest


class RunOnceSchemaTest(unittest.TestCase):
    """
    Ensure that any occurrence of 'run_once_' in roles/*/tasks/main.yml
    matches the pattern 'run_once_' + (role_name with '-' replaced by '_').
    """

    RUN_ONCE_PATTERN = re.compile(r"run_once_([A-Za-z0-9_]+)")

    def test_run_once_suffix_matches_role(self):
        # Determine project root: two levels up from this test file (tests/integration -> tests -> project)
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..')
        )
        violations = []

        # Find all roles/*/tasks/main.yml files
        pattern = os.path.join(project_root, 'roles', '*', 'tasks', 'main.yml')
        for filepath in glob.glob(pattern):
            # Extract role name from path
            parts = os.path.normpath(filepath).split(os.sep)
            try:
                role_index = parts.index('roles') + 1
                role_name = parts[role_index]
            except ValueError:
                continue  # skip unexpected path

            # Compute expected suffix
            expected_suffix = role_name.lower().replace('-', '_')

            # Read file content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find all run_once_ suffixes
            matches = self.RUN_ONCE_PATTERN.findall(content)
            if not matches:
                # No run_once_ in this file, skip
                continue

            # Check each occurrence
            for suffix in matches:
                if suffix != expected_suffix:
                    violations.append(
                        f"{filepath}: found run_once_{suffix}, expected run_once_{expected_suffix}"
                    )

        if violations:
            self.fail("Invalid run_once_ suffixes found:\n" + "\n".join(violations))


if __name__ == '__main__':
    unittest.main()
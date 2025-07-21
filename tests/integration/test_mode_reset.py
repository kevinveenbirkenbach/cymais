import os
import unittest

# Base directory for roles (adjust if needed)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../roles'))

class TestModeResetIntegration(unittest.TestCase):
    """
    Integration test to verify that when 'mode_reset' is used in any task file,
    the role provides a *_reset.yml (or reset.yml) and includes it correctly in main.yml,
    and that the include_tasks for that file with the mode_reset condition appears only once.
    """

    def test_mode_reset_tasks(self):
        for role_name in os.listdir(BASE_DIR):
            with self.subTest(role=role_name):
                role_path = os.path.join(BASE_DIR, role_name)
                tasks_dir = os.path.join(role_path, 'tasks')

                if not os.path.isdir(tasks_dir):
                    self.skipTest(f"Role '{role_name}' has no tasks directory.")

                # Look for 'mode_reset' in task files
                mode_reset_found = False
                for root, _, files in os.walk(tasks_dir):
                    for fname in files:
                        if not fname.lower().endswith(('.yml', '.yaml')):
                            continue
                        file_path = os.path.join(root, fname)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            if 'mode_reset' in f.read():
                                mode_reset_found = True
                                break
                    if mode_reset_found:
                        break

                if not mode_reset_found:
                    self.skipTest(f"Role '{role_name}': no mode_reset usage detected.")

                # Check *_reset.yml exists
                reset_files = [
                    fname for fname in os.listdir(tasks_dir)
                    if fname.endswith('_reset.yml') or fname == 'reset.yml'
                ]
                self.assertTrue(
                    reset_files,
                    f"Role '{role_name}': 'mode_reset' used but no *_reset.yml or reset.yml found in tasks/."
                )

                # Check main.yml exists
                main_yml = os.path.join(tasks_dir, 'main.yml')
                self.assertTrue(
                    os.path.isfile(main_yml),
                    f"Role '{role_name}': tasks/main.yml is missing."
                )

                with open(main_yml, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Match the actual reset file name used in include_tasks
                found_include = None
                for reset_file in reset_files:
                    if f'include_tasks: {reset_file}' in content:
                        found_include = reset_file
                        break

                self.assertIsNotNone(
                    found_include,
                    f"Role '{role_name}': tasks/main.yml must include one of {reset_files} with 'include_tasks'."
                )

                # Check the inclusion has the correct when condition
                include_line = f'include_tasks: {found_include}'
                when_line = 'when: mode_reset | bool'

                self.assertIn(
                    include_line,
                    content,
                    f"Role '{role_name}': tasks/main.yml missing '{include_line}'."
                )
                self.assertIn(
                    when_line,
                    content,
                    f"Role '{role_name}': tasks/main.yml missing '{when_line}'."
                )
                self.assertEqual(
                    content.count(include_line), 1,
                    f"Role '{role_name}': '{include_line}' must appear exactly once."
                )
                self.assertEqual(
                    content.count(when_line), 1,
                    f"Role '{role_name}': '{when_line}' must appear exactly once."
                )

if __name__ == '__main__':
    unittest.main(verbosity=2)

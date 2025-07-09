import os
import unittest
import yaml

# Base directory for roles (adjust if needed)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../roles'))

class TestModeResetIntegration(unittest.TestCase):
    """
    Integration test to verify that when 'mode_reset' is used in any task file,
    the role provides a reset.yml and includes it correctly in main.yml,
    and that the include_tasks for reset.yml with the mode_reset condition appears only once.
    """

    def test_mode_reset_tasks(self):
        # Iterate through each role directory
        for role_name in os.listdir(BASE_DIR):
            with self.subTest(role=role_name):
                role_path = os.path.join(BASE_DIR, role_name)
                tasks_dir = os.path.join(role_path, 'tasks')

                # Only consider directories with a tasks folder
                if not os.path.isdir(tasks_dir):
                    self.skipTest(f"Role '{role_name}' has no tasks directory.")

                # Simplified detection: check raw file content for 'mode_reset'
                mode_reset_found = False
                for root, _, files in os.walk(tasks_dir):
                    for fname in files:
                        if not fname.lower().endswith(('.yml', '.yaml')):
                            continue
                        file_path = os.path.join(root, fname)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        if 'mode_reset' in file_content:
                            mode_reset_found = True
                            break
                    if mode_reset_found:
                        break

                # If no mode_reset usage, skip this role
                if not mode_reset_found:
                    self.skipTest(f"Role '{role_name}': no mode_reset usage detected.")

                # 1) Check reset.yml exists
                reset_yml = os.path.join(tasks_dir, 'reset.yml')
                self.assertTrue(
                    os.path.isfile(reset_yml),
                    f"Role '{role_name}': 'mode_reset' used but tasks/reset.yml is missing."
                )

                # 2) Check inclusion in main.yml
                main_yml = os.path.join(tasks_dir, 'main.yml')
                self.assertTrue(
                    os.path.isfile(main_yml),
                    f"Role '{role_name}': tasks/main.yml is missing."
                )

                with open(main_yml, 'r', encoding='utf-8') as f:
                    content = f.read()

                include_line = 'include_tasks: reset.yml'
                when_line = 'when: mode_reset | bool'

                # Ensure the include and when lines are present
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

                # 3) Ensure the reset include with mode_reset appears only once
                include_count = content.count(include_line)
                when_count = content.count(when_line)
                self.assertEqual(
                    include_count, 1,
                    f"Role '{role_name}': 'include_tasks: reset.yml' must appear exactly once, found {include_count}."
                )
                self.assertEqual(
                    when_count, 1,
                    f"Role '{role_name}': 'when: mode_reset | bool' must appear exactly once, found {when_count}."
                )

if __name__ == '__main__':
    unittest.main(verbosity=2)

import os
import unittest
import yaml
import glob
import warnings

class TestApplicationIdMatchesRoleName(unittest.TestCase):
    def test_application_id_matches_role_directory(self):
        """
        Warn if application_id in vars/main.yml does not match
        the role directory basename, to avoid confusion.
        If vars/main.yml is missing, do nothing.
        """
        # locate the 'roles' directory (two levels up)
        base_dir = os.path.dirname(__file__)
        roles_dir = os.path.abspath(os.path.join(base_dir, '..', '..', 'roles'))

        # iterate over each role folder
        for role_path in glob.glob(os.path.join(roles_dir, '*')):
            if not os.path.isdir(role_path):
                continue

            role_name = os.path.basename(role_path)
            vars_main = os.path.join(role_path, 'vars', 'main.yml')

            # skip roles without vars/main.yml
            if not os.path.exists(vars_main):
                continue

            with open(vars_main, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}

            app_id = data.get('application_id')
            if app_id is None:
                warnings.warn(
                    f"{role_name}: 'application_id' is missing in vars/main.yml. "
                    f"Consider setting it to '{role_name}' to avoid confusion."
                )
            elif app_id != role_name:
                warnings.warn(
                    f"{role_name}: 'application_id' is '{app_id}', "
                    f"but the folder name is '{role_name}'. "
                    "This can lead to confusion—using the directory name "
                    "as the application_id is recommended."
                )

        # always pass
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()

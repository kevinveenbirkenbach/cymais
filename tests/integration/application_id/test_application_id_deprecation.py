import os
import unittest
import yaml
import warnings

# Dynamically determine the path to the roles directory
ROLES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'roles'))

class TestApplicationIdDeprecation(unittest.TestCase):
    def test_application_id_matches_role_name(self):
        """
        Deprecation: application_id in vars/main.yml must match the role name.
        """
        for role in os.listdir(ROLES_DIR):
            role_path = os.path.join(ROLES_DIR, role)
            vars_main_yml = os.path.join(role_path, 'vars', 'main.yml')
            if not os.path.isfile(vars_main_yml):
                continue
            with open(vars_main_yml, 'r', encoding='utf-8') as f:
                try:
                    data = yaml.safe_load(f)
                except Exception as e:
                    self.fail(f"Could not parse {vars_main_yml}: {e}")
            if not isinstance(data, dict):
                continue
            app_id = data.get('application_id')
            if app_id is not None and app_id != role:
                warnings.warn(
                    f"[DEPRECATION WARNING] application_id '{app_id}' in {vars_main_yml} "
                    f"does not match its role directory '{role}'.\n"
                    f"Please update 'application_id' to match the role name for future compatibility.",
                    DeprecationWarning
                )

if __name__ == "__main__":
    unittest.main()

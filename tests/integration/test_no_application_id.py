# tests/integration/test_no_application_id.py
import unittest
import yaml
import glob
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
test_files = glob.glob(os.path.join(BASE_DIR, "roles/sys-*/vars/main.yml"))

class TestNoApplicationId(unittest.TestCase):
    """
    Ensure that no sys-* role main.yml defines an application_id variable.
    """
    def test_no_application_id_defined(self):
        for file_path in test_files:
            with open(file_path, 'r') as f:
                content = yaml.safe_load(f) or {}

            self.assertNotIn(
                'application_id', content,
                f"Unexpected 'application_id' defined in {file_path}"
            )

if __name__ == '__main__':
    unittest.main()

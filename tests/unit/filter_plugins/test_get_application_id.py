# tests/unit/filter_plugins/test_get_application_id.py
import unittest
import os
import tempfile
import shutil
import yaml
from ansible.errors import AnsibleFilterError
from filter_plugins.get_application_id import get_application_id

class TestGetApplicationIdFilter(unittest.TestCase):
    def setUp(self):
        # Create a temporary project directory and switch to it
        self.tmpdir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.tmpdir)

        # Create the roles/testrole/vars directory structure
        self.role_name = 'testrole'
        self.vars_dir = os.path.join('roles', self.role_name, 'vars')
        os.makedirs(self.vars_dir)
        self.vars_file = os.path.join(self.vars_dir, 'main.yml')

    def tearDown(self):
        # Return to original cwd and remove temp directory
        os.chdir(self.original_cwd)
        shutil.rmtree(self.tmpdir)

    def write_vars_file(self, content):
        with open(self.vars_file, 'w') as f:
            yaml.dump(content, f)

    def test_returns_application_id(self):
        # Given a valid vars file with application_id
        expected_id = '12345'
        self.write_vars_file({'application_id': expected_id})
        # When
        result = get_application_id(self.role_name)
        # Then
        self.assertEqual(result, expected_id)

    def test_file_not_found_raises_error(self):
        # Given no vars file for a nonexistent role
        with self.assertRaises(AnsibleFilterError) as cm:
            get_application_id('nonexistent_role')
        self.assertIn("Vars file not found", str(cm.exception))

    def test_missing_key_raises_error(self):
        # Given a vars file without application_id
        self.write_vars_file({'other_key': 'value'})
        with self.assertRaises(AnsibleFilterError) as cm:
            get_application_id(self.role_name)
        self.assertIn("Key 'application_id' not found", str(cm.exception))

    def test_invalid_yaml_raises_error(self):
        # Write invalid YAML content
        with open(self.vars_file, 'w') as f:
            f.write(":::not a yaml:::")
        with self.assertRaises(AnsibleFilterError) as cm:
            get_application_id(self.role_name)
        self.assertIn("Error reading YAML", str(cm.exception))

if __name__ == '__main__':
    unittest.main()

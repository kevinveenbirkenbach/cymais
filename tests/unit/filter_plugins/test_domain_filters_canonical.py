import os
import sys
import unittest

# Add the filter_plugins directory to the import path
dir_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../filter_plugins')
)
sys.path.insert(0, dir_path)

from ansible.errors import AnsibleFilterError
from canonical_domains_map import FilterModule

class TestDomainFilters(unittest.TestCase):
    def setUp(self):
        self.filter_module = FilterModule()
        # Sample primary domain
        self.primary = 'example.com'

    def test_canonical_empty_apps(self):
        apps = {}
        expected = {}
        result = self.filter_module.canonical_domains_map(apps, self.primary)
        self.assertEqual(result, expected)

    def test_canonical_without_domains(self):
        apps = {'app1': {}}
        expected = {'app1': ['app1.example.com']}
        result = self.filter_module.canonical_domains_map(apps, self.primary)
        self.assertEqual(result, expected)

    def test_canonical_with_list(self):
        apps = {
            'app1': {
                'domains': {'canonical': ['foo.com', 'bar.com']}
            }
        }
        result = self.filter_module.canonical_domains_map(apps, self.primary)
        self.assertCountEqual(
            result['app1'],
            ['foo.com', 'bar.com']
        )

    def test_canonical_with_dict(self):
        apps = {
            'app1': {
                'domains': {'canonical': {'one': 'one.com', 'two': 'two.com'}}
            }
        }
        result = self.filter_module.canonical_domains_map(apps, self.primary)
        self.assertEqual(
            result['app1'],
            {'one': 'one.com', 'two': 'two.com'}
        )

    def test_canonical_duplicate_raises(self):
        apps = {
            'app1': {'domains': {'canonical': ['dup.com']}},
            'app2': {'domains': {'canonical': ['dup.com']}},
        }
        with self.assertRaises(AnsibleFilterError) as cm:
            self.filter_module.canonical_domains_map(apps, self.primary)
        # Updated to match new exception message
        self.assertIn("already configured for", str(cm.exception))

    def test_invalid_canonical_type(self):
        apps = {
            'app1': {'domains': {'canonical': 123}}
        }
        with self.assertRaises(AnsibleFilterError):
            self.filter_module.canonical_domains_map(apps, self.primary)

if __name__ == "__main__":
    unittest.main()
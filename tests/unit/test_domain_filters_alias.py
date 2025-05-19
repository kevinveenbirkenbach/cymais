import os
import sys
import unittest

# Add the filter_plugins directory to the import path
dir_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../filter_plugins')
)
sys.path.insert(0, dir_path)

from ansible.errors import AnsibleFilterError
from alias_domains_map import FilterModule

class TestDomainFilters(unittest.TestCase):
    def setUp(self):
        self.filter_module = FilterModule()
        # Sample primary domain
        self.primary = 'example.com'

    def test_alias_empty_apps(self):
        apps = {}
        expected = {}
        result = self.filter_module.alias_domains_map(apps, self.primary)
        self.assertEqual(result, expected)

    def test_alias_without_aliases_and_no_canonical(self):
        apps = {'app1': {}}
        # canonical defaults to ['app1.example.com'], so alias should be []
        expected = {'app1': []}
        result = self.filter_module.alias_domains_map(apps, self.primary)
        self.assertEqual(result, expected)

    def test_alias_with_explicit_aliases(self):
        apps = {
            'app1': {
                'domains': {'aliases': ['alias.com']}
            }
        }
        # canonical defaults to ['app1.example.com'], so alias should include alias.com and default
        expected = {'app1': ['alias.com', 'app1.example.com']}
        result = self.filter_module.alias_domains_map(apps, self.primary)
        self.assertCountEqual(result['app1'], expected['app1'])

    def test_alias_with_canonical_not_default(self):
        apps = {
            'app1': {
                'domains': {'canonical': ['foo.com']}
            }
        }
        # foo.com is canonical, default not in canonical so added as alias
        expected = {'app1': ['app1.example.com']}
        result = self.filter_module.alias_domains_map(apps, self.primary)
        self.assertEqual(result, expected)

    def test_alias_with_existing_default(self):
        apps = {
            'app1': {
                'domains': {
                    'canonical': ['foo.com'],
                    'aliases': ['app1.example.com']
                }
            }
        }
        # default present in aliases, should not be duplicated
        expected = {'app1': ['app1.example.com']}
        result = self.filter_module.alias_domains_map(apps, self.primary)
        self.assertEqual(result, expected)

    def test_invalid_aliases_type(self):
        apps = {
            'app1': {'domains': {'aliases': 123}}
        }
        with self.assertRaises(AnsibleFilterError):
            self.filter_module.alias_domains_map(apps, self.primary)

    def test_alias_with_empty_domains_cfg(self):
        apps = {
            'app1': {
                'domains': {}
            }
        }
        expected = apps
        result = self.filter_module.alias_domains_map(apps, self.primary)
        self.assertEqual(result, expected)
        
    def test_alias_with_canonical_dict_not_default(self):
        apps = {
            'app1': {
                'domains': {
                    'canonical': {
                        'one': 'one.com',
                        'two': 'two.com'
                    }
                }
            }
        }
        expected = {'app1': ['app1.example.com']}
        result = self.filter_module.alias_domains_map(apps, self.primary)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
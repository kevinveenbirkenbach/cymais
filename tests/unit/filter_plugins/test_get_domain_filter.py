# tests/unit/test_get_domain_filter.py
import unittest
import sys
import os

# Ensure filter_plugins directory is on the path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../../filter_plugins')
    )
)

from get_domain_filter import FilterModule
from ansible.errors import AnsibleFilterError

class TestGetDomainFilter(unittest.TestCase):
    def setUp(self):
        # Retrieve the get_domain filter function
        self.get_domain = FilterModule().filters()['get_domain']

    def test_string_value(self):
        domains = {'app': 'example.com'}
        self.assertEqual(self.get_domain(domains, 'app'), 'example.com')

    def test_dict_value(self):
        domains = {'app': {'primary': 'primary.com', 'secondary': 'secondary.com'}}
        self.assertEqual(self.get_domain(domains, 'app'), 'primary.com')

    def test_list_value(self):
        domains = {'app': ['first.com', 'second.com']}
        self.assertEqual(self.get_domain(domains, 'app'), 'first.com')

    def test_missing_application_id(self):
        domains = {'app': 'example.com'}
        with self.assertRaises(AnsibleFilterError):
            self.get_domain(domains, 'missing')

    def test_domains_not_dict(self):
        with self.assertRaises(AnsibleFilterError):
            self.get_domain(['not', 'a', 'dict'], 'app')

    def test_empty_string(self):
        domains = {'app': ''}
        with self.assertRaises(AnsibleFilterError):
            self.get_domain(domains, 'app')

    def test_empty_dict(self):
        domains = {'app': {}}
        with self.assertRaises(AnsibleFilterError):
            self.get_domain(domains, 'app')

    def test_empty_list(self):
        domains = {'app': []}
        with self.assertRaises(AnsibleFilterError):
            self.get_domain(domains, 'app')

    def test_non_string_in_dict(self):
        domains = {'app': {'key': 123}}
        with self.assertRaises(AnsibleFilterError):
            self.get_domain(domains, 'app')

    def test_non_string_in_list(self):
        domains = {'app': [123]}
        with self.assertRaises(AnsibleFilterError):
            self.get_domain(domains, 'app')

if __name__ == '__main__':
    unittest.main()

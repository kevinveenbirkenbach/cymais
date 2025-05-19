import unittest
import sys
import os

# Ensure filter_plugins directory is on the path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../filter_plugins'))
)

from generate_base_sld_domains import FilterModule

class TestGenerateBaseSldDomains(unittest.TestCase):
    def setUp(self):
        self.filter = FilterModule().generate_base_sld_domains

    def test_simple_string_and_redirect(self):
        domains = {'app': 'sub.example.com'}
        redirects = [{'source': 'alias.example.com'}]
        result = self.filter(domains, redirects)
        self.assertEqual(result, ['example.com'])

    def test_without_redirect_mappings(self):
        domains = {
            'a': 'a.co',
            'b': ['b.co', 'sub.c.co'],
            'c': {'x': 'x.co'}
        }
        result = self.filter(domains, None)
        self.assertEqual(result, ['a.co', 'b.co', 'c.co', 'x.co'])

    def test_redirect_list_sources(self):
        domains = {'app': 'app.domain.org'}
        redirects = [{'source': ['alias.domain.org', 'deep.sub.example.net']}]
        result = self.filter(domains, redirects)
        self.assertEqual(result, ['domain.org', 'example.net'])

    def test_duplicate_entries_and_sorting(self):
        domains = {
            'x': ['one.com', 'sub.one.com'],
            'y': 'two.com',
            'z': {'k': 'one.com'}
        }
        redirects = [{'source': 'deep.two.com'}]
        result = self.filter(domains, redirects)
        self.assertEqual(result, ['one.com', 'two.com'])

if __name__ == '__main__':
    unittest.main()

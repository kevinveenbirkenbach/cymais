import unittest
from filter_plugins.csp_filters import FilterModule

class TestCspFilters(unittest.TestCase):
    def setUp(self):
        self.filter = FilterModule()
        self.apps = {
            'app1': {
                'features': {
                    'oauth2': True,
                    'matomo': True,
                },
                'csp': {
                    'whitelist': {
                        'script-src': ['https://cdn.example.com'],
                        'connect-src': 'https://api.example.com',
                    },
                    'flags': {
                        'script-src': {
                            'unsafe_eval': True,
                            'unsafe_inline': False,
                        },
                        'style-src': {
                            'unsafe_inline': True,
                        },
                    },
                },
            },
            'app2': {}
        }
        self.domains = {
            'matomo': 'matomo.example.org'
        }

    def test_get_csp_whitelist_list(self):
        result = self.filter.get_csp_whitelist(self.apps, 'app1', 'script-src')
        self.assertEqual(result, ['https://cdn.example.com'])

    def test_get_csp_whitelist_string(self):
        result = self.filter.get_csp_whitelist(self.apps, 'app1', 'connect-src')
        self.assertEqual(result, ['https://api.example.com'])

    def test_get_csp_whitelist_none(self):
        result = self.filter.get_csp_whitelist(self.apps, 'app1', 'font-src')
        self.assertEqual(result, [])

    def test_get_csp_flags_eval(self):
        result = self.filter.get_csp_flags(self.apps, 'app1', 'script-src')
        self.assertIn("'unsafe-eval'", result)
        self.assertNotIn("'unsafe-inline'", result)

    def test_get_csp_flags_inline(self):
        result = self.filter.get_csp_flags(self.apps, 'app1', 'style-src')
        self.assertIn("'unsafe-inline'", result)
        self.assertNotIn("'unsafe-eval'", result)

    def test_get_csp_flags_none(self):
        result = self.filter.get_csp_flags(self.apps, 'app1', 'connect-src')
        self.assertEqual(result, [])

    def test_build_csp_header_basic(self):
        header = self.filter.build_csp_header(self.apps, 'app1', self.domains, web_protocol='https')
        # Ensure core directives are present
        self.assertIn("default-src 'self';", header)
        self.assertIn("script-src 'self' 'unsafe-eval' https://matomo.example.org https://cdn.example.com;", header)
        self.assertIn("connect-src 'self' https://matomo.example.org https://api.example.com;", header)
        self.assertTrue(header.strip().endswith('img-src * data: blob:;'))

    def test_build_csp_header_without_matomo_or_flags(self):
        header = self.filter.build_csp_header(self.apps, 'app2', self.domains)
        # default-src only contains 'self'
        self.assertIn("default-src 'self';", header)
        # no external URLs
        self.assertNotIn('http', header)
        # ends with img-src
        self.assertTrue(header.strip().endswith('img-src * data: blob:;'))

if __name__ == '__main__':
    unittest.main()
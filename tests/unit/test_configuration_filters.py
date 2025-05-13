# tests/unit/test_configuration_filters.py

import unittest
from filter_plugins.configuration_filters import (
    is_feature_enabled,
    get_csp_whitelist,
    get_csp_flags,
)


class TestConfigurationFilters(unittest.TestCase):
    def setUp(self):
        # Sample applications data for testing
        self.applications = {
            'app1': {
                'features': {
                    'oauth2': True,
                },
                'csp': {
                    'whitelist': {
                        # directive with a list
                        'script-src': ['https://example.com'],
                        # directive with a single string
                        'connect-src': 'https://api.example.com',
                    },
                    'flags': {
                        # both flags for script-src
                        'script-src': {
                            'unsafe_eval': True,
                            'unsafe_inline': False,
                        },
                        # only unsafe_inline for style-src
                        'style-src': {
                            'unsafe_inline': True,
                        },
                    },
                },
            },
            'app2': {
                # no features or csp defined
            },
        }

    # Tests for is_feature_enabled
    def test_is_feature_enabled_true(self):
        self.assertTrue(is_feature_enabled(self.applications, 'oauth2', 'app1'))

    def test_is_feature_enabled_false_missing_feature(self):
        self.assertFalse(is_feature_enabled(self.applications, 'nonexistent', 'app1'))

    def test_is_feature_enabled_false_missing_app(self):
        self.assertFalse(is_feature_enabled(self.applications, 'oauth2', 'unknown_app'))

    # Tests for get_csp_whitelist
    def test_get_csp_whitelist_returns_list_as_is(self):
        result = get_csp_whitelist(self.applications, 'app1', 'script-src')
        self.assertEqual(result, ['https://example.com'])

    def test_get_csp_whitelist_wraps_string_in_list(self):
        result = get_csp_whitelist(self.applications, 'app1', 'connect-src')
        self.assertEqual(result, ['https://api.example.com'])

    def test_get_csp_whitelist_empty_when_not_defined(self):
        result = get_csp_whitelist(self.applications, 'app1', 'frame-src')
        self.assertEqual(result, [])

    def test_get_csp_whitelist_empty_when_app_missing(self):
        result = get_csp_whitelist(self.applications, 'nonexistent_app', 'script-src')
        self.assertEqual(result, [])

    # Tests for get_csp_flags
    def test_get_csp_flags_includes_unsafe_eval(self):
        result = get_csp_flags(self.applications, 'app1', 'script-src')
        self.assertIn("'unsafe-eval'", result)
        self.assertNotIn("'unsafe-inline'", result)

    def test_get_csp_flags_includes_unsafe_inline(self):
        result = get_csp_flags(self.applications, 'app1', 'style-src')
        self.assertIn("'unsafe-inline'", result)
        self.assertNotIn("'unsafe-eval'", result)

    def test_get_csp_flags_empty_when_none_configured(self):
        result = get_csp_flags(self.applications, 'app1', 'connect-src')
        self.assertEqual(result, [])

    def test_get_csp_flags_empty_when_app_missing(self):
        result = get_csp_flags(self.applications, 'nonexistent_app', 'script-src')
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
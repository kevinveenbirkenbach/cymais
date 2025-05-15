# tests/unit/test_configuration_filters.py

import unittest
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    ),
)

from filter_plugins.configuration_filters import (
    is_feature_enabled,
)


class TestConfigurationFilters(unittest.TestCase):
    def setUp(self):
        # Sample applications data for testing
        self.applications = {
            'app1': {
                'features': {
                    'oauth2': True,
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

if __name__ == '__main__':
    unittest.main()
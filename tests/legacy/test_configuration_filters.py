import unittest
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    ),
)

from filter_plugins.get_app_conf import AppConfigKeyError, get_app_conf

def is_feature_enabled(applications: dict, feature: str, application_id: str) -> bool:
    """
    Wrapper for compatibility: Return True if applications[application_id].features[feature] is truthy.
    """
    return bool(get_app_conf(applications, application_id, f"features.{feature}", strict=False))


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
         with self.assertRaises(Exception):
            is_feature_enabled(self.applications, 'oauth2', 'unknown_app')

if __name__ == '__main__':
    unittest.main()
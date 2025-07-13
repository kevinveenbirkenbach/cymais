import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../filter_plugins')))

from get_app_conf import get_app_conf, AppConfigKeyError
from ansible.errors import AnsibleFilterError

class TestGetAppConf(unittest.TestCase):
    """
    Unit tests for the get_app_conf filter plugin function.
    Tests both strict and non-strict mode for positive and negative cases.
    """

    def setUp(self):
        """Set up a sample applications dict for all tests."""
        self.applications = {
            "myapp": {
                "features": {
                    "foo": True,
                    "bar": False,
                },
                "docker": {
                    "images": {
                        "myapp": "repo/myapp"
                    },
                    "versions": {
                        "myapp": "1.2.3"
                    }
                }
            }
        }

    def test_feature_enabled_strict_true_positive(self):
        """Test feature enabled (strict, present): should return True."""
        result = get_app_conf(self.applications, "myapp", "features.foo", strict=True)
        self.assertTrue(result)

    def test_feature_enabled_strict_true_negative(self):
        """Test feature enabled (strict, missing): should raise AnsibleFilterError."""
        with self.assertRaises(AnsibleFilterError) as ctx:
            get_app_conf(self.applications, "myapp", "features.baz", strict=True)
        self.assertIn("features.baz", str(ctx.exception))

    def test_feature_enabled_strict_false_positive(self):
        """Test feature enabled (non-strict, present): should return True."""
        result = get_app_conf(self.applications, "myapp", "features.foo", strict=False)
        self.assertTrue(result)

    def test_feature_enabled_strict_false_negative(self):
        """Test feature enabled (non-strict, missing): should return False, not error."""
        result = get_app_conf(self.applications, "myapp", "features.baz", strict=False)
        self.assertFalse(result)

    def test_docker_image_strict_true_positive(self):
        """Test docker image (strict, present): should return image name."""
        result = get_app_conf(self.applications, "myapp", "docker.images.myapp", strict=True)
        self.assertEqual(result, "repo/myapp")

    def test_docker_image_strict_true_negative(self):
        """Test docker image (strict, missing): should raise AnsibleFilterError."""
        with self.assertRaises(AnsibleFilterError) as ctx:
            get_app_conf(self.applications, "myapp", "docker.images.unknown", strict=True)
        self.assertIn("docker.images.unknown", str(ctx.exception))

    def test_docker_image_strict_false_positive(self):
        """Test docker image (non-strict, present): should return image name."""
        result = get_app_conf(self.applications, "myapp", "docker.images.myapp", strict=False)
        self.assertEqual(result, "repo/myapp")

    def test_docker_image_strict_false_negative(self):
        """Test docker image (non-strict, missing): should return False, not error."""
        result = get_app_conf(self.applications, "myapp", "docker.images.unknown", strict=False)
        self.assertFalse(result)

    def test_list_indexing_positive(self):
        """Test access of list index, present."""
        apps = {
            "app": {"foo": [{"bar": "x"}, {"bar": "y"}]}
        }
        result = get_app_conf(apps, "app", "foo[1].bar", strict=True)
        self.assertEqual(result, "y")

    def test_list_indexing_negative_strict_false(self):
        """Test access of list index, missing (non-strict): should return False."""
        apps = {
            "app": {"foo": [{"bar": "x"}]}
        }
        result = get_app_conf(apps, "app", "foo[1].bar", strict=False)
        self.assertFalse(result)

    def test_list_indexing_negative_strict_true(self):
        """Test access of list index, missing (strict): should raise error."""
        apps = {
            "app": {"foo": [{"bar": "x"}]}
        }
        with self.assertRaises(AnsibleFilterError):
            get_app_conf(apps, "app", "foo[1].bar", strict=True)

    def test_application_id_not_found(self):
        """Test with unknown application_id: should always raise error now."""
        with self.assertRaises(AppConfigKeyError):
            get_app_conf(self.applications, "unknown", "features.foo", strict=True)
        with self.assertRaises(AppConfigKeyError):
            get_app_conf(self.applications, "unknown", "features.foo", strict=False)
            
    def test_return_dict_strict_true(self):
        """Test that retrieving a dict value (strict) returns the dict itself."""
        result = get_app_conf(self.applications, "myapp", "docker.images", strict=True)
        expected = {
            "myapp": "repo/myapp"
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

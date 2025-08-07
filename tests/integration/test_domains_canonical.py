import unittest
import yaml
import glob
import os

class TestWebRolesDomains(unittest.TestCase):
    def test_canonical_domains_present_and_not_empty(self):
        """
        Check all roles/web-*/config/main.yml files:
        - must have domains.canonical defined
        - domains.canonical must not be empty dict, empty list, or empty string
        """
        role_config_paths = glob.glob("roles/web-*/config/main.yml")
        self.assertTrue(role_config_paths, "No roles/web-*/config/main.yml files found.")

        for path in role_config_paths:
            with self.subTest(role_config=path):
                with open(path, "r") as f:
                    data = yaml.safe_load(f)

                self.assertIsInstance(data, dict, f"YAML root is not a dict in {path}")

                domains = data.get('server',{}).get('domains',{})
                self.assertIsNotNone(domains, f"'domains' section missing in {path}")
                self.assertIsInstance(domains, dict, f"'domains' must be a dict in {path}")

                canonical = domains.get("canonical")
                self.assertIsNotNone(canonical, f"'server.domains.canonical' missing in {path}")

                # Check for emptiness
                empty_values = [{}, [], ""]
                self.assertNotIn(canonical, empty_values,
                    f"'server.domains.canonical' in {path} must not be empty dict, list, or empty string")

if __name__ == "__main__":
    unittest.main()

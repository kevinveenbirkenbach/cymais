import unittest
import os
import yaml

class TestNoStopRequiredIntegrity(unittest.TestCase):
    def setUp(self):
        self.roles_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../roles'))

    def test_no_stop_required_consistency(self):
        """
        This test ensures that if 'no_stop_required' is defined in any
        docker.services[*] entry, it must:
          - be a boolean value (True/False)
          - have a 'name' entry defined on the same level

        This is critical for the role 'sys-bkp-docker-2-loc', which uses the
        'no_stop_required' flag to determine which container names should be excluded
        from stopping during backup operations.

        The logic for processing this flag is implemented in:
        https://github.com/kevinveenbirkenbach/backup-docker-to-local
        """
        for role in os.listdir(self.roles_dir):
            docker_config_path = os.path.join(self.roles_dir, role, 'config', 'main.yml')
            if not os.path.isfile(docker_config_path):
                continue

            with open(docker_config_path, 'r') as f:
                try:
                    config = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    self.fail(f"YAML parsing failed for {docker_config_path}: {e}")
                    continue

            docker_services = (
                config.get('docker', {}).get('services', {}) if config else {}
            )

            for service_key, service in docker_services.items():
                if isinstance(service, dict) and 'no_stop_required' in service:
                    with self.subTest(role=role, service=service_key):
                        self.assertIsInstance(
                            service['no_stop_required'], bool,
                            f"'no_stop_required' in role '{role}', service '{service_key}' must be a boolean."
                        )
                        self.assertIn(
                            'name', service,
                            f"'name' is required in role '{role}', service '{service_key}' when 'no_stop_required' is set."
                        )

if __name__ == '__main__':
    unittest.main()

import unittest

# Import the filter module directly (adjust path as needed)
try:
    from filter_plugins.docker_service_enabled import FilterModule
except ModuleNotFoundError:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../filter_plugins')))
    from docker_service_enabled import FilterModule

class TestIsDockerServiceEnabledFilter(unittest.TestCase):
    def setUp(self):
        self.filter = FilterModule().filters()['is_docker_service_enabled']

    def test_enabled_true(self):
        applications = {
            'app1': {
                'docker': {
                    'services': {
                        'redis': {'enabled': True},
                        'database': {'enabled': True},
                    }
                }
            }
        }
        self.assertTrue(self.filter(applications, 'app1', 'redis'))
        self.assertTrue(self.filter(applications, 'app1', 'database'))

    def test_enabled_false(self):
        applications = {
            'app1': {
                'docker': {
                    'services': {
                        'redis': {'enabled': False},
                        'database': {'enabled': False},
                    }
                }
            }
        }
        self.assertFalse(self.filter(applications, 'app1', 'redis'))
        self.assertFalse(self.filter(applications, 'app1', 'database'))

    def test_missing_enabled_key(self):
        applications = {
            'app1': {
                'docker': {
                    'services': {
                        'redis': {},
                        'database': {},
                    }
                }
            }
        }
        self.assertFalse(self.filter(applications, 'app1', 'redis'))
        self.assertFalse(self.filter(applications, 'app1', 'database'))

    def test_missing_service_key(self):
        applications = {
            'app1': {
                'docker': {
                    'services': {
                        # no 'redis' or 'database'
                    }
                }
            }
        }
        self.assertFalse(self.filter(applications, 'app1', 'redis'))
        self.assertFalse(self.filter(applications, 'app1', 'database'))

    def test_missing_services_key(self):
        applications = {
            'app1': {
                'docker': {
                    # no 'services'
                }
            }
        }
        self.assertFalse(self.filter(applications, 'app1', 'redis'))

    def test_missing_docker_key(self):
        applications = {
            'app1': {
                # no 'docker'
            }
        }
        self.assertFalse(self.filter(applications, 'app1', 'database'))

    def test_missing_app_id(self):
        applications = {
            'other_app': {}
        }
        self.assertFalse(self.filter(applications, 'app1', 'redis'))

    def test_applications_is_none(self):
        applications = None
        self.assertFalse(self.filter(applications, 'app1', 'database'))

if __name__ == '__main__':
    unittest.main()

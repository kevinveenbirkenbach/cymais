import os
import sys
import unittest
from unittest.mock import patch, mock_open
from ansible.errors import AnsibleFilterError

# make sure our plugin is on PYTHONPATH
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../filter_plugins'))
sys.path.insert(0, root)

import load_configuration
from load_configuration import FilterModule, _cfg_cache

class TestLoadConfigurationFilter(unittest.TestCase):
    def setUp(self):
        _cfg_cache.clear()
        self.f = FilterModule().filters()['load_configuration']
        self.app = 'html_server'
        self.nested_cfg = {
            'html_server': {
                'features': {'matomo': True},
                'domains': {'canonical': ['html.example.com']}
            }
        }
        self.flat_cfg = {
            'features': {'matomo': False},
            'domains': {'canonical': ['flat.example.com']}
        }

    def test_invalid_key(self):
        with self.assertRaises(AnsibleFilterError):
            self.f(self.app, None)

    @patch('load_configuration.os.path.isdir', return_value=False)
    def test_no_roles_dir(self, _):
        with self.assertRaises(AnsibleFilterError):
            self.f(self.app, 'features.matomo')

    @patch('load_configuration.os.listdir', return_value=['r1'])
    @patch('load_configuration.os.path.isdir', return_value=True)
    @patch('load_configuration.os.path.exists', return_value=False)
    def test_no_matching_role(self, *_):
        self.assertIsNone(self.f(self.app, 'features.matomo'))

    @patch('load_configuration.os.listdir', return_value=['r1'])
    @patch('load_configuration.os.path.isdir', return_value=True)
    @patch('load_configuration.os.path.exists')
    @patch('load_configuration.open', new_callable=mock_open)
    @patch('load_configuration.yaml.safe_load')
    def test_primary_missing_conf(self, mock_yaml, mock_file, mock_exists, *_):
        mock_exists.side_effect = lambda p: p.endswith('vars/main.yml')
        mock_yaml.return_value = {'application_id': self.app}
        with self.assertRaises(AnsibleFilterError):
            self.f(self.app, 'features.matomo')

    @patch('load_configuration.os.listdir', return_value=['r1'])
    @patch('load_configuration.os.path.isdir', return_value=True)
    @patch('load_configuration.os.path.exists')
    @patch('load_configuration.open', new_callable=mock_open)
    @patch('load_configuration.yaml.safe_load')
    def test_primary_and_cache(self, mock_yaml, mock_file, mock_exists, *_):
        mock_exists.side_effect = lambda p: p.endswith('vars/main.yml') or p.endswith('vars/configuration.yml')
        mock_yaml.side_effect = [
            {'application_id': self.app},  # main.yml
            self.nested_cfg              # configuration.yml
        ]
        # first load
        self.assertTrue(self.f(self.app, 'features.matomo'))
        self.assertIn(self.app, _cfg_cache)
        mock_yaml.reset_mock()
        # from cache
        self.assertEqual(self.f(self.app, 'domains.canonical'),
                         ['html.example.com'])
        mock_yaml.assert_not_called()

    @patch('load_configuration.os.listdir', return_value=['r1'])
    @patch('load_configuration.os.path.isdir', return_value=True)
    @patch('load_configuration.os.path.exists', return_value=True)
    @patch('load_configuration.open', mock_open(read_data="html_server: {}"))
    @patch('load_configuration.yaml.safe_load', return_value={'html_server': {}})
    def test_key_not_found_after_load(self, *_):
        with self.assertRaises(AnsibleFilterError):
            self.f(self.app, 'does.not.exist')

    @patch('load_configuration.os.listdir', return_value=['r2'])
    @patch('load_configuration.os.path.isdir', return_value=True)
    @patch('load_configuration.os.path.exists')
    @patch('load_configuration.open', new_callable=mock_open)
    @patch('load_configuration.yaml.safe_load')
    def test_fallback_nested(self, mock_yaml, mock_file, mock_exists, *_):
        mock_exists.side_effect = lambda p: p.endswith('vars/configuration.yml')
        mock_yaml.return_value = self.nested_cfg
        # nested fallback must work
        self.assertTrue(self.f(self.app, 'features.matomo'))
        self.assertEqual(self.f(self.app, 'domains.canonical'),
                         ['html.example.com'])

    @patch('load_configuration.os.listdir', return_value=['r4'])
    @patch('load_configuration.os.path.isdir', return_value=True)
    @patch('load_configuration.os.path.exists')
    @patch('load_configuration.open', new_callable=mock_open)
    @patch('load_configuration.yaml.safe_load')
    def test_fallback_with_indexed_key(self, mock_yaml, mock_file, mock_exists, *_):
        # Testing with an indexed key like domains.canonical[0]
        mock_exists.side_effect = lambda p: p.endswith('vars/configuration.yml')
        mock_yaml.return_value = {
            'file-server': {
                'domains': {
                    'canonical': ['files.example.com', 'extra.example.com']
                }
            }
        }
        # should get the first element of the canonical domains list
        self.assertEqual(self.f('file-server', 'domains.canonical[0]'),
                         'files.example.com')

if __name__ == '__main__':
    unittest.main()

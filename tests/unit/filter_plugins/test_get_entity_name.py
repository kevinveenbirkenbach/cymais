import unittest
import tempfile
import shutil
import os
import sys
import yaml

class TestGetEntityNameFilter(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for roles and categories.yml
        self.temp_dir = tempfile.mkdtemp()
        self.roles_dir = os.path.join(self.temp_dir, 'roles')
        os.makedirs(self.roles_dir)
        self.categories_file = os.path.join(self.roles_dir, 'categories.yml')

        # Minimal categories.yml for tests
        categories = {
            'roles': {
                'web': {
                    'app': {
                        'title': "Applications",
                        'invokable': True
                    },
                    'svc': {
                        'title': "Services",
                        'invokable': True
                    }
                },
                'util': {
                    'desk': {
                        'dev': {
                            'title': "Dev Utilities",
                            'invokable': True
                        }
                    }
                },
                'sys': {
                    'bkp': {
                        'title': "Backup",
                        'invokable': True
                    },
                    'hlth': {
                        'title': "Health",
                        'invokable': True
                    }
                }
            }
        }
        with open(self.categories_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(categories, f, default_flow_style=False)

        # Patch working directory so plugin finds the test categories.yml
        self._cwd = os.getcwd()
        os.chdir(self.temp_dir)

        # Make sure filter_plugins directory is on sys.path
        plugin_path = os.path.join(self._cwd, "filter_plugins")
        if plugin_path not in sys.path and os.path.isdir(plugin_path):
            sys.path.insert(0, plugin_path)
        # Import plugin fresh each time
        global get_entity_name
        from filter_plugins.get_entity_name import get_entity_name

        self.get_entity_name = get_entity_name

    def tearDown(self):
        os.chdir(self._cwd)
        shutil.rmtree(self.temp_dir)

    def test_entity_name_web_app(self):
        self.assertEqual(self.get_entity_name("web-app-snipe-it"), "snipe-it")
        self.assertEqual(self.get_entity_name("web-app-nextcloud"), "nextcloud")
        self.assertEqual(self.get_entity_name("web-svc-file"), "file")

    def test_entity_name_util_desk_dev(self):
        self.assertEqual(self.get_entity_name("util-desk-dev-arduino"), "arduino")
        self.assertEqual(self.get_entity_name("util-desk-dev-shell"), "shell")

    def test_entity_name_sys_bkp(self):
        self.assertEqual(self.get_entity_name("sys-bkp-directory-validator"), "directory-validator")

    def test_entity_name_sys_hlth(self):
        self.assertEqual(self.get_entity_name("sys-hlth-btrfs"), "btrfs")

    def test_no_category_match(self):
        # Unknown category, should return input
        self.assertEqual(self.get_entity_name("foobar-role"), "foobar-role")

    def test_exact_category_match(self):
        self.assertEqual(self.get_entity_name("web-app"), "")

if __name__ == "__main__":
    unittest.main()

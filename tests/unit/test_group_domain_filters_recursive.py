import os
import tempfile
import shutil
import yaml
import unittest

# Import the filter module
import filter_plugins.group_domain_filters as gdf_module

class TestAddDomainIfGroupRecursive(unittest.TestCase):
    def setUp(self):
        # Create a temporary project structure
        self.tempdir = tempfile.mkdtemp()
        fp_dir = os.path.join(self.tempdir, 'filter_plugins')
        roles_dir = os.path.join(self.tempdir, 'roles')
        os.makedirs(fp_dir, exist_ok=True)
        os.makedirs(roles_dir, exist_ok=True)
        # Point module __file__ so plugin_dir resolves correctly
        gdf_module.__file__ = os.path.join(fp_dir, 'group_domain_filters.py')
        self.roles_dir = roles_dir

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def write_role(self, role_name, dependencies, application_id):
        """
        Helper: write a role directory with meta/main.yml and vars/main.yml
        """
        meta_dir = os.path.join(self.roles_dir, role_name, 'meta')
        vars_dir = os.path.join(self.roles_dir, role_name, 'vars')
        os.makedirs(meta_dir, exist_ok=True)
        os.makedirs(vars_dir, exist_ok=True)
        # Write meta/main.yml
        with open(os.path.join(meta_dir, 'main.yml'), 'w') as f:
            yaml.safe_dump({'dependencies': dependencies}, f)
        # Write vars/main.yml
        with open(os.path.join(vars_dir, 'main.yml'), 'w') as f:
            yaml.safe_dump({'application_id': application_id}, f)

    def test_direct_application_id_in_group_names(self):
        # If domain_key (application_id) is directly in group_names
        result = gdf_module.FilterModule.add_domain_if_group({}, 'app1', 'domain1', ['app1'])
        self.assertEqual(result, {'app1': 'domain1'})

    def test_indirect_dependency_application_id(self):
        # roleA depends on roleB; roleB has application_id 'appB'
        self.write_role('roleA', ['roleB'], 'appA')
        self.write_role('roleB', [], 'appB')
        # group_names includes roleA, so appB should be reachable
        result = gdf_module.FilterModule.add_domain_if_group({}, 'appB', 'domainB', ['roleA'])
        self.assertEqual(result, {'appB': 'domainB'})

    def test_multi_level_dependency_application_id(self):
        # roleX -> roleY -> roleZ; roleZ id is 'appZ'
        self.write_role('roleX', ['roleY'], 'appX')
        self.write_role('roleY', ['roleZ'], 'appY')
        self.write_role('roleZ', [], 'appZ')
        # Starting from roleX, appZ reachable
        result = gdf_module.FilterModule.add_domain_if_group({}, 'appZ', 'domainZ', ['roleX'])
        self.assertEqual(result, {'appZ': 'domainZ'})

    def test_domain_key_for_parent_role(self):
        # roleParent has app 'appP', and depends on roleChild('appC')
        self.write_role('roleParent', ['roleChild'], 'appP')
        self.write_role('roleChild', [], 'appC')
        # Even appP reachable via deps of roleParent (including itself)
        result = gdf_module.FilterModule.add_domain_if_group({}, 'appP', 'domainP', ['roleParent'])
        self.assertEqual(result, {'appP': 'domainP'})

    def test_no_inclusion_for_unrelated(self):
        # Unrelated roles
        self.write_role('roleC', ['roleD'], 'appC')
        self.write_role('roleD', [], 'appD')
        # group_names does not include 'roleC' or 'roleD'
        result = gdf_module.FilterModule.add_domain_if_group({}, 'appC', 'domainC', ['otherRole'])
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()

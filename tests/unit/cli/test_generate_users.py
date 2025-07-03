import os
import sys
import unittest
import tempfile
import shutil
import yaml
from collections import OrderedDict

# Add cli/ to import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..", "cli")))

import generate_users

class TestGenerateUsers(unittest.TestCase):
    def test_build_users_auto_increment_and_overrides(self):
        defs = {
            'alice': {},
            'bob': {'uid': 2000, 'email': 'bob@custom.com', 'description': 'Custom user'},
            'carol': {}
        }
        users = generate_users.build_users(
            defs=defs,
            primary_domain='example.com',
            start_id=1001,
            become_pwd='pw'
        )
        # alice should get uid/gid 1001
        self.assertEqual(users['alice']['uid'], 1001)
        self.assertEqual(users['alice']['gid'], 1001)
        self.assertEqual(users['alice']['email'], 'alice@example.com')
        # bob overrides
        self.assertEqual(users['bob']['uid'], 2000)
        self.assertEqual(users['bob']['gid'], 2000)
        self.assertEqual(users['bob']['email'], 'bob@custom.com')
        self.assertIn('description', users['bob'])
        # carol should get next free id = 1002
        self.assertEqual(users['carol']['uid'], 1002)
        self.assertEqual(users['carol']['gid'], 1002)

    def test_build_users_default_lookup_password(self):
        """
        When no 'password' override is provided,
        the become_pwd lookup template string must be used as the password.
        """
        defs = {'frank': {}}
        lookup_template = '{{ lookup("password", "/dev/null length=42 chars=ascii_letters,digits") }}'
        users = generate_users.build_users(
            defs=defs,
            primary_domain='example.com',
            start_id=1001,
            become_pwd=lookup_template
        )
        self.assertEqual(
            users['frank']['password'],
            lookup_template,
            "The lookup template string was not correctly applied as the default password"
        )

    def test_build_users_override_password(self):
        """
        When a 'password' override is provided,
        that custom password must be used instead of become_pwd.
        """
        defs = {'eva': {'password': 'custompw'}}
        lookup_template = '{{ lookup("password", "/dev/null length=42 chars=ascii_letters,digits") }}'
        users = generate_users.build_users(
            defs=defs,
            primary_domain='example.com',
            start_id=1001,
            become_pwd=lookup_template
        )
        self.assertEqual(
            users['eva']['password'],
            'custompw',
            "The override password was not correctly applied"
        )


    def test_build_users_duplicate_override_uid(self):
        defs = {
            'u1': {'uid': 1001},
            'u2': {'uid': 1001}
        }
        with self.assertRaises(ValueError):
            generate_users.build_users(defs, 'ex.com', 1001, 'pw')

    def test_build_users_shared_gid_allowed(self):
        # Allow two users to share the same GID when one overrides gid and the other uses that as uid
        defs = {
            'a': {'uid': 1500},
            'b': {'gid': 1500}
        }
        users = generate_users.build_users(defs, 'ex.com', 1500, 'pw')
        # Both should have gid 1500
        self.assertEqual(users['a']['gid'], 1500)
        self.assertEqual(users['b']['gid'], 1500)

    def test_build_users_duplicate_username_email(self):
        defs = {
            'u1': {'username': 'same', 'email': 'same@ex.com'},
            'u2': {'username': 'same'}
        }
        # second user with same username should raise
        with self.assertRaises(ValueError):
            generate_users.build_users(defs, 'ex.com', 1001, 'pw')

    def test_dictify_converts_ordereddict(self):
        od = generate_users.OrderedDict([('a', 1), ('b', {'c': 2})])
        result = generate_users.dictify(OrderedDict(od))
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {'a': 1, 'b': {'c': 2}})

    def test_load_user_defs_and_conflict(self):
        # create temp roles structure
        tmp = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(tmp, 'role1/meta'))
            os.makedirs(os.path.join(tmp, 'role2/meta'))
            # role1 defines user x
            with open(os.path.join(tmp, 'role1/meta/users.yml'), 'w') as f:
                yaml.safe_dump({'users': {'x': {'email': 'x@a'}}}, f)
            # role2 defines same user x with same value
            with open(os.path.join(tmp, 'role2/meta/users.yml'), 'w') as f:
                yaml.safe_dump({'users': {'x': {'email': 'x@a'}}}, f)
            defs = generate_users.load_user_defs(tmp)
            self.assertIn('x', defs)
            # now conflict definition
            with open(os.path.join(tmp, 'role2/meta/users.yml'), 'w') as f:
                yaml.safe_dump({'users': {'x': {'email': 'x@b'}}}, f)
            with self.assertRaises(ValueError):
                generate_users.load_user_defs(tmp)
        finally:
            shutil.rmtree(tmp)

if __name__ == '__main__':
    unittest.main()

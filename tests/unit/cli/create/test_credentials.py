import os
import sys
import unittest
from unittest import mock

# Ensure cli module is importable
dir_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../cli')
)
sys.path.insert(0, dir_path)

# Import functions and classes to test
from cli.create.credentials import ask_for_confirmation, main
from utils.handler.vault import VaultHandler, VaultScalar
import subprocess
import tempfile
import yaml

class TestCreateCredentials(unittest.TestCase):
    def test_ask_for_confirmation_yes(self):
        with mock.patch('builtins.input', return_value='y'):
            self.assertTrue(ask_for_confirmation('test_key'))

    def test_ask_for_confirmation_no(self):
        with mock.patch('builtins.input', return_value='n'):
            self.assertFalse(ask_for_confirmation('test_key'))

    def test_vault_encrypt_string_success(self):
        handler = VaultHandler('dummy_pw_file')
        # Mock subprocess.run to simulate successful vault encryption
        fake_output = 'Encrypted data'
        completed = subprocess.CompletedProcess(
            args=['ansible-vault'], returncode=0, stdout=fake_output, stderr=''
        )
        with mock.patch('subprocess.run', return_value=completed) as proc_run:
            result = handler.encrypt_string('plain_val', 'name')
            proc_run.assert_called_once()
            self.assertEqual(result, fake_output)

    def test_vault_encrypt_string_failure(self):
        handler = VaultHandler('dummy_pw_file')
        # Mock subprocess.run to simulate failure
        completed = subprocess.CompletedProcess(
            args=['ansible-vault'], returncode=1, stdout='', stderr='error')
        with mock.patch('subprocess.run', return_value=completed):
            with self.assertRaises(RuntimeError):
                handler.encrypt_string('plain_val', 'name')

    def test_main_overrides_and_file_writing(self):
        # Setup temporary files for role-path vars and inventory
        with tempfile.TemporaryDirectory() as tmpdir:
            role_path = os.path.join(tmpdir, 'role')
            os.makedirs(os.path.join(role_path, 'config'))
            os.makedirs(os.path.join(role_path, 'schema'))
            os.makedirs(os.path.join(role_path, 'vars'))
            # Create vars/main.yml with application_id
            main_vars = {'application_id': 'app_test'}
            with open(os.path.join(role_path, 'vars', 'main.yml'), 'w') as f:
                yaml.dump(main_vars, f)
            # Create config/main.yml with features disabled
            config = {'features': {'central_database': False}}
            with open(os.path.join(role_path, "config" , "main.yml"), 'w') as f:
                yaml.dump(config, f)
            # Create schema.yml defining plain credential
            schema = {'credentials': {'api_key': {'description': 'API key', 'algorithm': 'plain', 'validation': {}}}}
            with open(os.path.join(role_path, 'schema', 'main.yml'), 'w') as f:
                yaml.dump(schema, f)
            # Prepare inventory file
            inventory_file = os.path.join(tmpdir, 'inventory.yml')
            with open(inventory_file, 'w') as f:
                yaml.dump({}, f)
            vault_pw_file = os.path.join(tmpdir, 'pw.txt')
            with open(vault_pw_file, 'w') as f:
                f.write('pw')

            # Simulate ansible-vault encrypt_string output for api_key
            fake_snippet = "!vault |\n  $ANSIBLE_VAULT;1.1;AES256\n    ENCRYPTEDVALUE"
            completed = subprocess.CompletedProcess(
                args=['ansible-vault'], returncode=0, stdout=fake_snippet, stderr=''
            )
            with mock.patch('subprocess.run', return_value=completed):
                # Run main with override for credentials.api_key and force to skip prompt
                sys.argv = [
                    'create/credentials.py',
                    '--role-path', role_path,
                    '--inventory-file', inventory_file,
                    '--vault-password-file', vault_pw_file,
                    '--set', 'credentials.api_key=SECRET',
                    '--force'
                ]
                # Should complete without error
                main()
                # Verify inventory file updated with vaulted api_key
                data = yaml.safe_load(open(inventory_file))
                creds = data['applications']['app_test']['credentials']
                self.assertIn('api_key', creds)
                # VaultScalar serializes to a vault block, safe_load returns a string containing the vault header
                self.assertIsInstance(creds['api_key'], str)
                self.assertTrue(creds['api_key'].lstrip().startswith('$ANSIBLE_VAULT'))

if __name__ == '__main__':
    unittest.main()

import os
import sys
import tempfile
import unittest
import shutil
import yaml
from pathlib import Path
from unittest.mock import patch

# Ensure cli directory is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../cli")))

import generate_vaulted_credentials as gvc


class TestGenerateVaultedCredentials(unittest.TestCase):
    def setUp(self):
        # Create temporary directory structure for a fake role and inventory
        self.temp_dir = tempfile.mkdtemp()
        self.role_path = Path(self.temp_dir) / "roles" / "docker-demoapp"
        self.meta_path = self.role_path / "meta"
        self.meta_path.mkdir(parents=True)

        # Define schema with no "applications" root (direct app-specific structure)
        self.schema = {
            "credentials": {
                "shared_secret": {
                    "description": "A shared secret",
                    "algorithm": "sha256",
                    "validation": "^[a-f0-9]{64}$"
                },
                "postgresql_secret": {
                    "description": "Postgres password",
                    "algorithm": "bcrypt",
                    "validation": "^\\$2[aby]\\$.{56}$"
                }
            }
        }

        with open(self.meta_path / "schema.yml", "w") as f:
            yaml.dump(self.schema, f)

        # Create an empty inventory file
        self.inventory_path = Path(self.temp_dir) / "host_vars" / "testhost.yml"
        self.inventory_path.parent.mkdir(parents=True)
        with open(self.inventory_path, "w") as f:
            f.write("")

        self.vault_mock = "$ANSIBLE_VAULT;1.1;AES256\nmockedvaultdata=="

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_apply_schema_creates_vaulted_credentials(self):
        schema_data = gvc.load_yaml_file(self.meta_path / "schema.yml")
        inventory_data = gvc.load_yaml_file(self.inventory_path)

        with patch("generate_vaulted_credentials.encrypt_with_vault") as mock_encrypt:
            mock_encrypt.return_value = self.vault_mock
            updated = gvc.apply_schema_to_inventory(
                schema=schema_data,
                inventory_data=inventory_data,
                app_id="demoapp",
                overrides={},
                vault_password_file="dummy",
                ask_vault_pass=False
            )

        # Expect credentials to be written under applications.demoapp
        self.assertIn("applications", updated)
        self.assertIn("demoapp", updated["applications"])
        creds = updated["applications"]["demoapp"]["credentials"]
        self.assertIn("shared_secret", creds)
        self.assertIn("postgresql_secret", creds)

        for key in creds:
            self.assertTrue(str(creds[key]).startswith("!vault") or "$ANSIBLE_VAULT" in str(creds[key]))

    def test_existing_key_prompts_before_overwriting(self):
        # Pre-populate the inventory with one value
        pre_existing = {
            "applications": {
                "demoapp": {
                    "credentials": {
                        "shared_secret": "unchanged"
                    }
                }
            }
        }
        gvc.save_yaml_file(self.inventory_path, pre_existing)

        schema_data = gvc.load_yaml_file(self.meta_path / "schema.yml")
        inventory_data = gvc.load_yaml_file(self.inventory_path)

        with patch("generate_vaulted_credentials.encrypt_with_vault") as mock_encrypt, \
             patch("builtins.input", return_value="n"):
            mock_encrypt.return_value = self.vault_mock
            updated = gvc.apply_schema_to_inventory(
                schema=schema_data,
                inventory_data=inventory_data,
                app_id="demoapp",
                overrides={},
                vault_password_file="dummy",
                ask_vault_pass=False
            )

        # Value should remain unchanged
        self.assertEqual(updated["applications"]["demoapp"]["credentials"]["shared_secret"], "unchanged")

    def test_set_override_applies_correctly(self):
        schema_data = gvc.load_yaml_file(self.meta_path / "schema.yml")
        inventory_data = gvc.load_yaml_file(self.inventory_path)

        override_value = "custom-override-value"
        override_key = "credentials.shared_secret"

        # Patch vault encryption to just return the plaintext prefixed as mock
        with patch("generate_vaulted_credentials.encrypt_with_vault") as mock_encrypt:
            mock_encrypt.side_effect = lambda val, name, **kwargs: f"$ANSIBLE_VAULT;1.1;AES256\n{val}"
            updated = gvc.apply_schema_to_inventory(
                schema=schema_data,
                inventory_data=inventory_data,
                app_id="demoapp",
                overrides={override_key: override_value},
                vault_password_file="dummy",
                ask_vault_pass=False
            )

        actual = updated["applications"]["demoapp"]["credentials"]["shared_secret"]
        self.assertIn(override_value, str(actual), "The override value was not used during encryption.")

if __name__ == "__main__":
    unittest.main()

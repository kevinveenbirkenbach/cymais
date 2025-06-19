import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

# Ensure the cli package is on sys.path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../cli")
    ),
)

from utils.handler.yaml import YamlHandler
from utils.handler.vault import VaultHandler, VaultScalar
from cli.utils.manager.inventory import InventoryManager


class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for role and inventory files
        self.tmpdir = Path(tempfile.mkdtemp())

        # Patch YamlHandler.load_yaml
        self.load_yaml_patcher = patch.object(
            YamlHandler,
            'load_yaml',
            side_effect=self.fake_load_yaml
        )
        self.load_yaml_patcher.start()

        # Patch VaultHandler.encrypt_string with correct signature
        self.encrypt_patcher = patch.object(
            VaultHandler,
            'encrypt_string',
            new=lambda self, plain, key: f"{key}: !vault |\n    encrypted_{plain}"
        )
        self.encrypt_patcher.start()

    def tearDown(self):
        # Stop patchers
        patch.stopall()
        # Remove temporary directory
        shutil.rmtree(self.tmpdir)

    def fake_load_yaml(self, path):
        path = Path(path)
        # Return schema for meta/schema.yml
        if path.match("*/meta/schema.yml"):
            return {
                "credentials": {
                    "plain_cred": {"description": "desc", "algorithm": "plain", "validation": {}},
                    "nested": {"inner": {"description": "desc2", "algorithm": "sha256", "validation": {}}}
                }
            }
        # Return application_id for vars/main.yml
        if path.match("*/vars/main.yml"):
            return {"application_id": "testapp"}
        # Return feature flags for vars/configuration.yml
        if path.match("*/vars/configuration.yml"):
            return {"features": {"central_database": True}}
        # Return empty inventory for inventory.yml
        if path.name == "inventory.yml":
            return {}
        raise FileNotFoundError(f"Unexpected load_yaml path: {path}")

    def test_load_application_id_missing(self):
        """Loading application_id without it should raise SystemExit."""
        role_dir = self.tmpdir / "role"
        (role_dir / "vars").mkdir(parents=True)
        (role_dir / "vars" / "main.yml").write_text("{}")

        with patch.object(YamlHandler, 'load_yaml', return_value={}):
            with self.assertRaises(SystemExit):
                InventoryManager(role_dir, self.tmpdir / "inventory.yml", "pw", {}).load_application_id(role_dir)

    def test_generate_value_algorithms(self):
        """Verify generate_value produces outputs of the expected form."""
        # Bypass __init__ to avoid YAML loading
        im = InventoryManager.__new__(InventoryManager)

        # random_hex → 64 bytes hex = 128 chars
        hex_val = im.generate_value("random_hex")
        self.assertEqual(len(hex_val), 128)
        self.assertTrue(all(c in "0123456789abcdef" for c in hex_val))

        # sha256 → 64 hex chars
        sha256_val = im.generate_value("sha256")
        self.assertEqual(len(sha256_val), 64)

        # sha1 → 40 hex chars
        sha1_val = im.generate_value("sha1")
        self.assertEqual(len(sha1_val), 40)

        # bcrypt → starts with bcrypt prefix
        bcrypt_val = im.generate_value("bcrypt")
        self.assertTrue(bcrypt_val.startswith("$2"))

        # alphanumeric → 64 chars
        alnum = im.generate_value("alphanumeric")
        self.assertEqual(len(alnum), 64)
        self.assertTrue(alnum.isalnum())

        # base64_prefixed_32 → starts with "base64:"
        b64 = im.generate_value("base64_prefixed_32")
        self.assertTrue(b64.startswith("base64:"))

    def test_apply_schema_and_recurse(self):
        """
        apply_schema should inject central_database password and vault nested.inner
        """
        # Setup role directory
        role_dir = self.tmpdir / "role"
        (role_dir / "meta").mkdir(parents=True)
        (role_dir / "vars").mkdir(parents=True)

        # Create empty inventory.yml
        inv_file = self.tmpdir / "inventory.yml"
        inv_file.write_text(" ")

        # Provide override for plain_cred to avoid SystemExit
        overrides = {'credentials.plain_cred': 'OVERRIDE_PLAIN'}

        # Instantiate manager with overrides
        mgr = InventoryManager(role_dir, inv_file, "pw", overrides=overrides)

        # Patch generate_value locally for predictable values
        with patch.object(InventoryManager, 'generate_value', lambda self, alg: f"GEN_{alg}"):
            result = mgr.apply_schema()

        apps = result["applications"]["testapp"]
        # central_database entry
        self.assertEqual(apps["credentials"]["database_password"], "GEN_alphanumeric")
        # plain_cred vaulted from override
        self.assertIsInstance(apps["credentials"]["plain_cred"], VaultScalar)
        # nested.inner should not be vaulted due to code's prefix check
        self.assertEqual(
            apps["credentials"]["nested"]["inner"],
            {"description": "desc2", "algorithm": "sha256", "validation": {}},
        )

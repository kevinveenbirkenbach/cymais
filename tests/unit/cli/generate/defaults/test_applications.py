import os
import unittest
import tempfile
import shutil
import yaml
from pathlib import Path
import subprocess


class TestGenerateDefaultApplications(unittest.TestCase):
    def setUp(self):
        # Create temp role structure
        self.temp_dir = Path(tempfile.mkdtemp())
        self.roles_dir = self.temp_dir / "roles"
        self.roles_dir.mkdir()

        # Sample role
        self.sample_role = self.roles_dir / "web-app-testapp"
        (self.sample_role / "vars").mkdir(parents=True)
        (self.sample_role / "config").mkdir(parents=True)

        # Write application_id and configuration
        (self.sample_role / "vars" / "main.yml").write_text("application_id: testapp\n")
        (self.sample_role / "config" / "main.yml").write_text("foo: bar\nbaz: 123\n")

        # Output file path
        self.output_file = self.temp_dir / "group_vars" / "all" / "04_applications.yml"

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_script_generates_expected_yaml(self):
        script_path = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "cli/build/defaults/applications.py"

        result = subprocess.run(
            [
                "python3", str(script_path),
                "--roles-dir", str(self.roles_dir),
                "--output-file", str(self.output_file)
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertTrue(self.output_file.exists(), "Output file was not created.")

        data = yaml.safe_load(self.output_file.read_text())
        self.assertIn("defaults_applications", data)
        self.assertIn("testapp", data["defaults_applications"])
        self.assertEqual(data["defaults_applications"]["testapp"]["foo"], "bar")
        self.assertEqual(data["defaults_applications"]["testapp"]["baz"], 123)
        
    def test_missing_config_adds_empty_defaults(self):
        """
        If a role has vars/main.yml but no config/main.yml,
        the generator should still create an entry with an empty dict.
        """
        # Create a role with vars/main.yml but without config/main.yml
        role_no_config = self.roles_dir / "role-no-config"
        (role_no_config / "vars").mkdir(parents=True)
        (role_no_config / "vars" / "main.yml").write_text("application_id: noconfigapp\n")

        # Run the generator
        result = subprocess.run(
            ["python3", str(self.script_path),
             "--roles-dir", str(self.roles_dir),
             "--output-file", str(self.output_file)],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

        # Verify the output YAML
        data = yaml.safe_load(self.output_file.read_text())
        apps = data.get("defaults_applications", {})

        # The new application_id must exist and be an empty dict
        self.assertIn("noconfigapp", apps)
        self.assertEqual(apps["noconfigapp"], {})

    def test_no_config_directory_adds_empty_defaults(self):
        """
        If a role has vars/main.yml but no config directory at all,
        the generator should still emit an empty-dict entry.
        """
        # Create a role with vars/main.yml but do not create config/ at all
        role_no_cfg_dir = self.roles_dir / "role-no-cfg-dir"
        (role_no_cfg_dir / "vars").mkdir(parents=True)
        (role_no_cfg_dir / "vars" / "main.yml").write_text("application_id: nocfgdirapp\n")
        # Note: no config/ directory is created here

        # Run the generator again
        result = subprocess.run(
            ["python3", str(self.script_path),
             "--roles-dir", str(self.roles_dir),
             "--output-file", str(self.output_file)],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

        # Load and inspect the output
        data = yaml.safe_load(self.output_file.read_text())
        apps = data.get("defaults_applications", {})

        # Ensure that the application_id appears with an empty mapping
        self.assertIn("nocfgdirapp", apps)
        self.assertEqual(apps["nocfgdirapp"], {})


if __name__ == "__main__":
    unittest.main()

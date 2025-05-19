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
        self.sample_role = self.roles_dir / "docker-testapp"
        (self.sample_role / "vars").mkdir(parents=True)

        # Write application_id and configuration
        (self.sample_role / "vars" / "main.yml").write_text("application_id: testapp\n")
        (self.sample_role / "vars" / "configuration.yml").write_text("foo: bar\nbaz: 123\n")

        # Output file path
        self.output_file = self.temp_dir / "group_vars" / "all" / "03_applications.yml"

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_script_generates_expected_yaml(self):
        script_path = Path(__file__).resolve().parent.parent.parent / "cli" / "generate-applications-defaults.py"

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


if __name__ == "__main__":
    unittest.main()

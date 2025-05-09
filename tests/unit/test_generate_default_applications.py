import os
import unittest
import tempfile
import shutil
import yaml
from pathlib import Path
from unittest.mock import patch
import importlib.util

class TestGenerateDefaultApplications(unittest.TestCase):
    def setUp(self):
        # Determine script location
        self.script_path = Path(__file__).resolve().parent.parent.parent / "cli" / "generate_default_applications.py"
        spec = importlib.util.spec_from_file_location("generate_default_applications", self.script_path)
        self.gda = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.gda)

        # Setup fake Ansible role structure
        self.temp_dir = Path(tempfile.mkdtemp())
        self.roles_dir = self.temp_dir / "roles"
        self.output_file = self.temp_dir / "group_vars" / "all" / "11_applications.yml"
        (self.roles_dir / "docker-testapp" / "vars").mkdir(parents=True, exist_ok=True)
        (self.roles_dir / "docker-testapp" / "tasks").mkdir(parents=True, exist_ok=True)

        # Populate vars/main.yml and vars/configuration.yml
        (self.roles_dir / "docker-testapp" / "vars" / "main.yml").write_text("application_id: testapp\n")
        (self.roles_dir / "docker-testapp" / "vars" / "configuration.yml").write_text("foo: bar\nbaz: 123\n")
        (self.roles_dir / "docker-testapp" / "tasks" / "main.yml").write_text("# dummy task")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_extracts_and_writes_configuration(self):
        self.gda.generate_default_applications(
            roles_dir=self.roles_dir,
            output_file=self.output_file
        )

        self.assertTrue(self.output_file.exists())
        result = yaml.safe_load(self.output_file.read_text())
        self.assertIn("testapp", result)
        self.assertEqual(result["testapp"]["foo"], "bar")
        self.assertEqual(result["testapp"]["baz"], 123)

if __name__ == "__main__":
    unittest.main()
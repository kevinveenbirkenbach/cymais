import os
import sys
import json
import tempfile
import shutil
import unittest
from unittest.mock import patch

# Import the script as a module (assumes the script is named tree.py)
SCRIPT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../cli/build/tree.py")
)

class TestTreeShadowFolder(unittest.TestCase):
    def setUp(self):
        # Create temp roles dir and a dummy role
        self.roles_dir = tempfile.mkdtemp()
        self.role_name = "dummyrole"
        self.role_path = os.path.join(self.roles_dir, self.role_name)
        os.makedirs(os.path.join(self.role_path, "meta"))

        # Prepare shadow dir
        self.shadow_dir = tempfile.mkdtemp()

        # Patch sys.argv for the script
        self.orig_argv = sys.argv[:]
        sys.argv = [
            SCRIPT_PATH,
            "-d", self.roles_dir,
            "-s", self.shadow_dir,
            "-o", "json"
        ]

    def tearDown(self):
        sys.argv = self.orig_argv
        shutil.rmtree(self.roles_dir)
        shutil.rmtree(self.shadow_dir)

    @patch("cli.build.tree.build_mappings")
    @patch("cli.build.tree.output_graph")
    def test_tree_json_written_to_shadow_folder(self, mock_output_graph, mock_build_mappings):
        # Prepare dummy graph
        dummy_graph = {"dummy": {"test": 42}}
        mock_build_mappings.return_value = dummy_graph

        # Run the script (as __main__)
        import runpy
        runpy.run_path(SCRIPT_PATH, run_name="__main__")

        # Check file in shadow folder
        expected_tree_path = os.path.join(
            self.shadow_dir, self.role_name, "meta", "tree.json"
        )
        self.assertTrue(os.path.isfile(expected_tree_path), "tree.json not found in shadow folder")

        # Check contents
        with open(expected_tree_path) as f:
            data = json.load(f)
        self.assertEqual(data, dummy_graph, "tree.json content mismatch")

        # Ensure nothing was written to original meta/
        original_tree_path = os.path.join(self.role_path, "meta", "tree.json")
        self.assertFalse(os.path.isfile(original_tree_path), "tree.json should NOT be in role's meta/")

if __name__ == "__main__":
    unittest.main()

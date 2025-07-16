import os
import sys
import tempfile
import unittest
from unittest import mock

# Insert project root into import path so we can import main.py
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

import main  # assumes main.py lives at the project root


class TestMainHelpers(unittest.TestCase):
    def test_format_command_help_basic(self):
        name = "cmd"
        description = "A basic description"
        output = main.format_command_help(
            name, description,
            indent=2, col_width=20, width=40
        )
        # Should start with two spaces and the command name
        self.assertTrue(output.startswith("  cmd"))
        # Description should appear somewhere in the wrapped text
        self.assertIn("A basic description", output)

    def test_list_cli_commands_filters_and_sorts(self):
        # Create a temporary directory with sample files containing argparse
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create Python files that import argparse
            one_path = os.path.join(tmpdir, "one.py")
            with open(one_path, "w") as f:
                f.write("import argparse\n# dummy CLI command\n")

            two_path = os.path.join(tmpdir, "two.py")
            with open(two_path, "w") as f:
                f.write("import argparse\n# another CLI command\n")

            # Non-Python and dunder files should be ignored
            open(os.path.join(tmpdir, "__init__.py"), "w").close()
            open(os.path.join(tmpdir, "ignore.txt"), "w").close()

            # Only 'one' and 'two' should be returned, in sorted order
            commands = main.list_cli_commands(tmpdir)
            self.assertEqual([(None, 'one'), (None, 'two')], commands)

    def test_git_clean_repo_invokes_git_clean(self):
        with mock.patch('main.subprocess.run') as mock_run:
            main.git_clean_repo()
            mock_run.assert_called_once_with(['git', 'clean', '-Xfd'], check=True)

    @mock.patch('main.subprocess.run')
    def test_extract_description_via_help_with_description(self, mock_run):
        # Simulate subprocess returning help output with a description
        mock_stdout = "usage: dummy.py [options]\n\nThis is a help description.\n"
        mock_run.return_value = mock.Mock(stdout=mock_stdout)
        description = main.extract_description_via_help("/fake/path/dummy.py")
        self.assertEqual(description, "This is a help description.")

    @mock.patch('main.subprocess.run')
    def test_extract_description_via_help_without_description(self, mock_run):
        # Simulate subprocess returning help output without a description
        mock_stdout = "usage: empty.py [options]\n"
        mock_run.return_value = mock.Mock(stdout=mock_stdout)
        description = main.extract_description_via_help("/fake/path/empty.py")
        self.assertEqual(description, "-")


if __name__ == "__main__":
    unittest.main()

# tests/unit/test_main.py

import os
import sys
import stat
import tempfile
import unittest

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
        # Create a temporary directory with sample files
        with tempfile.TemporaryDirectory() as tmpdir:
            open(os.path.join(tmpdir, "one.py"), "w").close()
            open(os.path.join(tmpdir, "__init__.py"), "w").close()
            open(os.path.join(tmpdir, "ignore.txt"), "w").close()
            open(os.path.join(tmpdir, "two.py"), "w").close()

            # Only 'one' and 'two' should be returned, in sorted order
            commands = main.list_cli_commands(tmpdir)
            self.assertEqual(commands, ["one", "two"])

    def test_extract_description_via_help_with_description(self):
        # Create a dummy script that prints a help description
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, "dummy.py")
            with open(script_path, "w") as f:
                f.write(
                    "#!/usr/bin/env python3\n"
                    "import sys\n"
                    "if '--help' in sys.argv:\n"
                    "    print('usage: dummy.py [options]')\n"
                    "    print()\n"
                    "    print('This is a help description.')\n"
                )
            # Make it executable
            mode = os.stat(script_path).st_mode
            os.chmod(script_path, mode | stat.S_IXUSR)

            description = main.extract_description_via_help(script_path)
            self.assertEqual(description, "This is a help description.")

    def test_extract_description_via_help_without_description(self):
        # Script that has no help description
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, "empty.py")
            with open(script_path, "w") as f:
                f.write(
                    "#!/usr/bin/env python3\n"
                    "print('no help here')\n"
                )
            description = main.extract_description_via_help(script_path)
            self.assertEqual(description, "-")


if __name__ == "__main__":
    unittest.main()

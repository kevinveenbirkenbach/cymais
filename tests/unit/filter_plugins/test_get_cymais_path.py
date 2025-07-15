# tests/unit/filter_plugins/test_get_cymais_path.py

import unittest
import sys
import os

# Ensure the filter_plugins directory is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../filter_plugins')))

from get_cymais_path import get_cymais_dir, get_cymais_file
from ansible.errors import AnsibleFilterError


class TestGetCymaisPath(unittest.TestCase):
    def test_valid_input(self):
        """Test valid input with exactly one underscore"""
        self.assertEqual(get_cymais_dir("web_app"), "web")
        self.assertEqual(get_cymais_file("web_app"), "app")

        self.assertEqual(get_cymais_dir("sys_timer"), "sys")
        self.assertEqual(get_cymais_file("sys_timer"), "timer")

    def test_invalid_no_underscore(self):
        """Test input with no underscore raises error"""
        with self.assertRaises(AnsibleFilterError):
            get_cymais_dir("invalid")
        with self.assertRaises(AnsibleFilterError):
            get_cymais_file("invalid")

    def test_invalid_multiple_underscores(self):
        """Test input with more than one underscore raises error"""
        with self.assertRaises(AnsibleFilterError):
            get_cymais_dir("too_many_parts_here")
        with self.assertRaises(AnsibleFilterError):
            get_cymais_file("too_many_parts_here")

    def test_empty_string(self):
        """Test empty string input raises error"""
        with self.assertRaises(AnsibleFilterError):
            get_cymais_dir("")
        with self.assertRaises(AnsibleFilterError):
            get_cymais_file("")


if __name__ == '__main__':
    unittest.main()

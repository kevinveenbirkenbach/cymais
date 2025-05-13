import unittest
from unittest.mock import patch
import subprocess
import sys
import os

# 🧩 Add the path to the script under test
SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../roles/health-csp/files"))
sys.path.insert(0, SCRIPT_PATH)

import health_csp

class TestHealthCspScript(unittest.TestCase):

    @patch("os.listdir")
    def test_extract_domains_valid_files(self, mock_listdir):
        mock_listdir.return_value = ["example.com.conf", "sub.example.com.conf", "invalid.conf~"]
        domains = health_csp.extract_domains("/dummy/path")
        self.assertEqual(domains, ["example.com", "sub.example.com"])

    @patch("os.listdir", side_effect=FileNotFoundError)
    def test_extract_domains_missing_dir(self, _):
        result = health_csp.extract_domains("/invalid/path")
        self.assertIsNone(result)

    @patch("subprocess.run")
    def test_run_node_checker_success(self, mock_run):
        mock_run.return_value.returncode = 0
        code = health_csp.run_node_checker("/some/script.js", ["example.com"])
        self.assertEqual(code, 0)

    @patch("subprocess.run", side_effect=subprocess.CalledProcessError(3, "node"))
    def test_run_node_checker_failure(self, _):
        code = health_csp.run_node_checker("/some/script.js", ["fail.com"])
        self.assertEqual(code, 3)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path

class TestInitFiles(unittest.TestCase):
    def test_all_test_dirs_have_init(self):
        """
        Ensure every subdirectory in the 'tests' folder (excluding '__pycache__') contains an '__init__.py' file.
        """
        tests_root = Path(__file__).resolve().parents[2] / "tests"

        for path in tests_root.rglob("*"):
            if path.is_dir() and "__pycache__" not in path.parts:
                init_file = path / "__init__.py"
                with self.subTest(directory=str(path.relative_to(tests_root))):
                    self.assertTrue(
                        init_file.exists(),
                        f"Missing __init__.py in directory: {path}"
                    )

if __name__ == "__main__":
    unittest.main()

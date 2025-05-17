import unittest
import sys
import os

# Ensure filter_plugins directory is on the path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../filter_plugins'))
)

from safe import safe_placeholders

class TestSafePlaceholdersFilter(unittest.TestCase):
    def test_simple_replacement(self):
        template = "Hello, {user}!"
        mapping = {'user': 'Alice'}
        self.assertEqual(safe_placeholders(template, mapping), "Hello, Alice!")

    def test_missing_placeholder(self):
        template = "Hello, {user}!"
        # Missing placeholder should raise KeyError
        with self.assertRaises(KeyError):
            safe_placeholders(template, {})

    def test_none_template(self):
        self.assertEqual(safe_placeholders(None, {'user': 'Alice'}), "")

    def test_no_placeholders(self):
        template = "Just a plain string"
        mapping = {'any': 'value'}
        self.assertEqual(safe_placeholders(template, mapping), "Just a plain string")

    def test_multiple_placeholders(self):
        template = "{greet}, {user}!"
        mapping = {'greet': 'Hi', 'user': 'Bob'}
        self.assertEqual(safe_placeholders(template, mapping), "Hi, Bob!")

    def test_numeric_values(self):
        template = "Count: {n}"
        mapping = {'n': 0}
        self.assertEqual(safe_placeholders(template, mapping), "Count: 0")

    def test_extra_mapping_keys(self):
        template = "Value: {a}"
        mapping = {'a': '1', 'b': '2'}
        self.assertEqual(safe_placeholders(template, mapping), "Value: 1")

    def test_malformed_template(self):
        # Unclosed placeholder should be caught and return empty string
        template = "Unclosed {key"
        mapping = {'key': 'value'}
        self.assertEqual(safe_placeholders(template, mapping), "")

    def test_mapping_none(self):
        template = "Test {x}"
        self.assertEqual(safe_placeholders(template, None), "")

if __name__ == '__main__':
    unittest.main()

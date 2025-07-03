import unittest
import sys
import os
from jinja2 import Undefined

# Ensure filter_plugins directory is on the path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../filter_plugins'))
)

from safe import FilterModule

class TestSafeVarFilter(unittest.TestCase):
    def setUp(self):
        # Retrieve the safe_var filter function
        self.filter = FilterModule().filters()['safe_var']

    def test_returns_non_empty_string(self):
        self.assertEqual(self.filter('hello'), 'hello')

    def test_returns_empty_string(self):
        self.assertEqual(self.filter(''), '')

    def test_returns_empty_for_none(self):
        self.assertEqual(self.filter(None), '')

    def test_returns_empty_for_jinja_undefined(self):
        # Instantiate an Undefined without arguments
        undef = Undefined()
        self.assertEqual(self.filter(undef), '')

    def test_returns_zero_for_zero(self):
        # 0 is falsey but not None or Undefined, so safe_var returns it
        self.assertEqual(self.filter(0), 0)

    def test_returns_list_and_dict_unchanged(self):
        data = {'key': 'value'}
        self.assertEqual(self.filter(data), data)
        lst = [1, 2, 3]
        self.assertEqual(self.filter(lst), lst)

if __name__ == '__main__':
    unittest.main()

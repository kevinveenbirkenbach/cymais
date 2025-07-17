import unittest
from filter_plugins.get_public_id import FilterModule

class TestGetPublicId(unittest.TestCase):
    def setUp(self):
        self.filter = FilterModule().filters()['get_public_id']

    def test_extract_public_id(self):
        self.assertEqual(self.filter("svc-user-abc123"), "abc123")
        self.assertEqual(self.filter("something-simple-xyz"), "xyz")
        self.assertEqual(self.filter("a-b-c-d-e"), "e")

    def test_no_hyphen(self):
        with self.assertRaises(ValueError):
            self.filter("nohyphenhere")

    def test_non_string_input(self):
        with self.assertRaises(ValueError):
            self.filter(12345)

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            self.filter("")

if __name__ == '__main__':
    unittest.main()

import unittest

from filter_plugins.group_domain_filters import FilterModule

class TestAddDomainIfGroup(unittest.TestCase):
    def setUp(self):
        self.filter = FilterModule().filters()["add_domain_if_group"]

    def test_add_string_value(self):
        result = self.filter({}, "akaunting", "accounting.example.org", ["akaunting"])
        self.assertEqual(result, {"akaunting": "accounting.example.org"})

    def test_add_list_value(self):
        result = self.filter({}, "mastodon", ["microblog.example.org"], ["mastodon"])
        self.assertEqual(result, {"mastodon": ["microblog.example.org"]})

    def test_add_dict_value(self):
        result = self.filter({}, "bluesky", {"web": "bskyweb.example.org", "api": "bluesky.example.org"}, ["bluesky"])
        self.assertEqual(result, {"bluesky": {"web": "bskyweb.example.org", "api": "bluesky.example.org"}})

    def test_ignore_if_not_in_group(self):
        result = self.filter({}, "akaunting", "accounting.example.org", ["wordpress"])
        self.assertEqual(result, {})

    def test_merge_with_existing(self):
        initial = {"wordpress": ["blog.example.org"]}
        result = self.filter(initial, "akaunting", "accounting.example.org", ["akaunting"])
        self.assertEqual(result, {
            "wordpress": ["blog.example.org"],
            "akaunting": "accounting.example.org"
        })

    def test_dict_is_not_mutated(self):
        base = {"keycloak": "auth.example.org"}
        copy = dict(base)  # make a copy for comparison
        _ = self.filter(base, "akaunting", "accounting.example.org", ["akaunting"])
        self.assertEqual(base, copy)  # original must stay unchanged

    def test_multiple_adds_accumulate(self):
        result = {}
        result = self.filter(result, "akaunting", "accounting.example.org", ["akaunting", "wordpress"])
        result = self.filter(result, "wordpress", ["blog.example.org"], ["akaunting", "wordpress"])
        result = self.filter(result, "bluesky", {"web": "bskyweb.example.org", "api": "bluesky.example.org"}, ["bluesky"])
        self.assertEqual(result, {
            "akaunting": "accounting.example.org",
            "wordpress": ["blog.example.org"],
            "bluesky": {"web": "bskyweb.example.org", "api": "bluesky.example.org"},
        })

if __name__ == "__main__":
    unittest.main()

import unittest
import hashlib
import base64
from filter_plugins.csp_filters import FilterModule, AnsibleFilterError

class TestCspFilters(unittest.TestCase):
    def setUp(self):
        self.filter = FilterModule()
        self.apps = {
            'app1': {
                'features': {
                    'oauth2': True,
                    'matomo': True,
                },
                'csp': {
                    'whitelist': {
                        'script-src': ['https://cdn.example.com'],
                        'connect-src': 'https://api.example.com',
                    },
                    'flags': {
                        'script-src': {
                            'unsafe-eval': True,
                            'unsafe-inline': False,
                        },
                        'style-src': {
                            'unsafe-inline': True,
                        },
                    },
                    'hashes': {
                        'script-src': [
                            "console.log('hello');",
                        ],
                        'style-src': [
                            "body { background: #fff; }",
                        ]
                    }
                },
            },
            'app2': {}
        }
        self.domains = {
            'matomo': 'matomo.example.org'
        }

    def test_get_csp_whitelist_list(self):
        result = self.filter.get_csp_whitelist(self.apps, 'app1', 'script-src')
        self.assertEqual(result, ['https://cdn.example.com'])

    def test_get_csp_whitelist_string(self):
        result = self.filter.get_csp_whitelist(self.apps, 'app1', 'connect-src')
        self.assertEqual(result, ['https://api.example.com'])

    def test_get_csp_whitelist_none(self):
        result = self.filter.get_csp_whitelist(self.apps, 'app1', 'font-src')
        self.assertEqual(result, [])

    def test_get_csp_flags_eval(self):
        result = self.filter.get_csp_flags(self.apps, 'app1', 'script-src')
        self.assertIn("'unsafe-eval'", result)
        self.assertNotIn("'unsafe-inline'", result)

    def test_get_csp_flags_inline(self):
        result = self.filter.get_csp_flags(self.apps, 'app1', 'style-src')
        self.assertIn("'unsafe-inline'", result)
        self.assertNotIn("'unsafe-eval'", result)

    def test_get_csp_flags_none(self):
        result = self.filter.get_csp_flags(self.apps, 'app1', 'connect-src')
        self.assertEqual(result, [])

    def test_build_csp_header_basic(self):
        header = self.filter.build_csp_header(self.apps, 'app1', self.domains, web_protocol='https')
        # Ensure core directives are present
        self.assertIn("default-src 'self';", header)
        # script-src directive should include unsafe-eval, Matomo domain and CDN (hash may follow)
        self.assertIn(
            "script-src 'self' 'unsafe-eval' https://matomo.example.org https://cdn.example.com",
            header
        )
        # connect-src directive unchanged (no inline hash)
        self.assertIn(
            "connect-src 'self' https://matomo.example.org https://api.example.com;",
            header
        )
        # ends with img-src
        self.assertTrue(header.strip().endswith('img-src * data: blob:;'))

    def test_build_csp_header_without_matomo_or_flags(self):
        header = self.filter.build_csp_header(self.apps, 'app2', self.domains)
        # default-src only contains 'self'
        self.assertIn("default-src 'self';", header)
        # no external URLs
        self.assertNotIn('http', header)
        # ends with img-src
        self.assertTrue(header.strip().endswith('img-src * data: blob:;'))
        
    def test_get_csp_inline_content_list(self):
        snippets = self.filter.get_csp_inline_content(self.apps, 'app1', 'script-src')
        self.assertEqual(snippets, ["console.log('hello');"])

    def test_get_csp_inline_content_string(self):
        # simulate single string instead of list
        self.apps['app1']['csp']['hashes']['style-src'] = "body { color: red; }"
        snippets = self.filter.get_csp_inline_content(self.apps, 'app1', 'style-src')
        self.assertEqual(snippets, ["body { color: red; }"])

    def test_get_csp_inline_content_none(self):
        snippets = self.filter.get_csp_inline_content(self.apps, 'app1', 'font-src')
        self.assertEqual(snippets, [])

    def test_get_csp_hash_known_value(self):
        content = "alert(1);"
        # compute expected
        digest = hashlib.sha256(content.encode('utf-8')).digest()
        b64 = base64.b64encode(digest).decode('utf-8')
        expected = f"'sha256-{b64}'"
        result = self.filter.get_csp_hash(content)
        self.assertEqual(result, expected)

    def test_get_csp_hash_error(self):
        with self.assertRaises(AnsibleFilterError):
            # passing a non-decodable object
            self.filter.get_csp_hash(None)

    def test_build_csp_header_includes_hashes(self):
        header = self.filter.build_csp_header(self.apps, 'app1', self.domains, web_protocol='https')
        # check that the script-src directive includes our inline hash
        script_hash = self.filter.get_csp_hash("console.log('hello');")
        self.assertIn(script_hash, header)
        # check that the style-src directive includes its inline hash
        style_hash = self.filter.get_csp_hash("body { background: #fff; }")
        self.assertIn(style_hash, header)

if __name__ == '__main__':
    unittest.main()
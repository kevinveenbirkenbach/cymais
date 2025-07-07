import re
import warnings
import unittest
from pathlib import Path

class TestDockerComposeTemplates(unittest.TestCase):
    # Search for all roles/*/templates/docker-compose.yml.j2
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    TEMPLATE_PATTERN = 'roles/*/templates/docker-compose.yml.j2'

    # Allowed lines before BASE_INCLUDE
    ALLOWED_BEFORE_BASE = [
        re.compile(r'^\s*$'),                # empty line
        re.compile(r'^\s*version:.*$'),      # version: ...
        re.compile(r'^\s*#.*$'),             # YAML comment
        re.compile(r'^\s*\{\#.*\#\}\s*$'),    # Jinja comment {# ... #}
    ]

    BASE_INCLUDE = "{% include 'roles/docker-compose/templates/base.yml.j2' %}"
    NET_INCLUDE = "{% include 'roles/docker-compose/templates/networks.yml.j2' %}"

    def test_docker_compose_includes(self):
        """
        Verifies for each found docker-compose.yml.j2:
        1. BASE_INCLUDE and NET_INCLUDE are present exactly once
        2. BASE_INCLUDE appears before NET_INCLUDE
        3. Only allowed lines appear before BASE_INCLUDE (invalid lines issue warnings)
        """
        template_paths = sorted(
            self.PROJECT_ROOT.glob(self.TEMPLATE_PATTERN)
        )
        self.assertTrue(template_paths, f"No templates found for pattern {self.TEMPLATE_PATTERN}")

        for template_path in template_paths:
            with self.subTest(template=template_path):
                content = template_path.read_text(encoding='utf-8')
                lines = content.splitlines()

                # Check each include occurs exactly once
                count_base = lines.count(self.BASE_INCLUDE)
                self.assertEqual(
                    count_base,
                    1,
                    f"{template_path}: '{self.BASE_INCLUDE}' occurs {count_base} times, expected once"
                )
                count_net = lines.count(self.NET_INCLUDE)
                self.assertEqual(
                    count_net,
                    1,
                    f"{template_path}: '{self.NET_INCLUDE}' occurs {count_net} times, expected once"
                )

                # Find BASE_INCLUDE index
                idx_base = lines.index(self.BASE_INCLUDE)
                # Find NET_INCLUDE index
                idx_net = lines.index(self.NET_INCLUDE)

                # Check order
                self.assertLess(
                    idx_base,
                    idx_net,
                    f"{template_path}: '{self.BASE_INCLUDE}' must come before '{self.NET_INCLUDE}'"
                )

                # Warn on invalid lines before BASE_INCLUDE
                for i, line in enumerate(lines[:idx_base]):
                    if not any(pat.match(line) for pat in self.ALLOWED_BEFORE_BASE):
                        warnings.warn(
                            f"{template_path}: Invalid line before {self.BASE_INCLUDE} (line {i+1}): {line!r}",
                            category=RuntimeWarning
                        )

if __name__ == '__main__':
    unittest.main()

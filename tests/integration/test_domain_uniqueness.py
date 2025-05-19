import unittest
import yaml
import subprocess
from pathlib import Path
from collections import Counter

class TestDomainUniqueness(unittest.TestCase):
    def test_no_duplicate_domains(self):
        """
        Load the applications YAML (generating it via `make build` if missing),
        collect all entries under domains.canonical and domains.aliases across all applications,
        and assert that no domain appears more than once.
        """
        repo_root = Path(__file__).resolve().parents[2]
        yaml_file = repo_root / 'group_vars' / 'all' / '03_applications.yml'

        # Generate the file if it doesn't exist
        if not yaml_file.exists():
            subprocess.run(['make', 'build'], cwd=repo_root, check=True)

        # Load the applications configuration
        cfg = yaml.safe_load(yaml_file.read_text(encoding='utf-8')) or {}
        apps = cfg.get('defaults_applications', {})

        all_domains = []
        for app_name, app_cfg in apps.items():
            domains_cfg = app_cfg.get('domains', {})

            # canonical entries may be a list or a mapping
            canonical = domains_cfg.get('canonical', [])
            if isinstance(canonical, dict):
                values = list(canonical.values())
            else:
                values = canonical or []
            all_domains.extend(values)

            # aliases entries may be a list or a mapping
            aliases = domains_cfg.get('aliases', [])
            if isinstance(aliases, dict):
                values = list(aliases.values())
            else:
                values = aliases or []
            all_domains.extend(values)

        # Filter out any empty or non-string entries
        domain_list = [d for d in all_domains if isinstance(d, str) and d.strip()]
        counts = Counter(domain_list)

        # Find duplicates
        duplicates = [domain for domain, count in counts.items() if count > 1]
        if duplicates:
            self.fail(f"Duplicate domain entries found: {duplicates}\n (May 'make build' solves this issue.)")

if __name__ == "__main__":
    unittest.main()

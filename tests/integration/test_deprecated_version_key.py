import unittest
from pathlib import Path
import yaml

class TestDeprecatedVersionKey(unittest.TestCase):
    def test_version_key_deprecation(self):
        """
        Checks all roles/web-app-*/vars/configuration.yml for deprecated use of 'version'.
        Warns if 'version' is set but 'images' is missing.
        Prints warnings but does NOT fail the test.
        """
        repo_root = Path(__file__).resolve().parent.parent.parent
        roles_dir = repo_root / "roles"
        warnings = []

        for role_path in roles_dir.iterdir():
            if not (role_path.is_dir() and role_path.name.startswith("web-app-")):
                continue

            cfg_file = role_path / "vars" / "configuration.yml"
            if not cfg_file.exists():
                continue

            try:
                config = yaml.safe_load(cfg_file.read_text("utf-8")) or {}
            except yaml.YAMLError as e:
                print(f"YAML parse error in {cfg_file}: {e}")
                continue

            uses_version = 'version' in config
            uses_images = 'images' in config

            if uses_version:
                warnings.append(
                    f"[DEPRECATION WARNING] {role_path.name}/vars/configuration.yml: "
                    f"'version' is deprecated. Replace it by docker.versions[version]."
                )
            if uses_images:
                warnings.append(
                    f"[DEPRECATION WARNING] {role_path.name}/vars/configuration.yml: "
                    f"'images' is deprecated. Replace it by docker.images[image]."
                )

        if warnings:
            print("\n".join(warnings))
        else:
            print("No deprecated 'version:' keys found in docker roles without 'images:'.")

        # Never fail, just warn
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()

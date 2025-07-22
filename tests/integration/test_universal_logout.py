import unittest
import glob
import yaml

class TestUniversalLogoutSetting(unittest.TestCase):
    ROLES_PATH = "roles/web-app-*/config/main.yml"

    def test_universal_logout_defined(self):
        files = glob.glob(self.ROLES_PATH)
        self.assertGreater(len(files), 0, f"No role config files found under {self.ROLES_PATH}")

        errors = []

        for file_path in files:
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    errors.append(f"YAML parse error in '{file_path}': {e}")
                    continue

            features = {}
            if data is not None:
                features = data.get("features", {})

            if "universal_logout" not in features:
                errors.append(
                    f"Missing 'universal_logout' setting in features of '{file_path}'. "
                    "You must explicitly set 'universal_logout' to true or false for this app."
                )
            else:
                val = features["universal_logout"]
                if not isinstance(val, bool):
                    errors.append(
                        f"The 'universal_logout' setting in '{file_path}' must be boolean true or false, "
                        f"but found: {val} (type {type(val).__name__})"
                    )

        if errors:
            self.fail("\n\n".join(errors))


if __name__ == "__main__":
    unittest.main()

import os
import yaml
import unittest
from pathlib import Path

ROLES_DIR = Path(__file__).resolve().parent.parent.parent / "roles"


class TestApplicationIdConsistency(unittest.TestCase):
    def test_application_id_matches_docker_prefix(self):
        failed_roles = []

        for role_path in ROLES_DIR.iterdir():
            if role_path.name in ["docker-container","docker-compose", "docker-central-database", "docker-repository-setup"]:
                continue
            
            if role_path.is_dir() and role_path.name.startswith("docker-"):
                expected_id = role_path.name.replace("docker-", "", 1)
                vars_file = role_path / "vars" / "main.yml"

                if not vars_file.exists():
                    failed_roles.append((role_path.name, "vars/main.yml missing"))
                    continue

                with open(vars_file, "r") as f:
                    try:
                        vars_data = yaml.safe_load(f) or {}
                    except yaml.YAMLError as e:
                        failed_roles.append((role_path.name, f"YAML error: {e}"))
                        continue

                actual_id = vars_data.get("application_id")
                if actual_id != expected_id:
                    failed_roles.append((role_path.name, f"application_id is '{actual_id}', expected '{expected_id}'"))

        if failed_roles:
            msg = "\n".join([f"{role}: {reason}" for role, reason in failed_roles])
            self.fail(f"The following roles have mismatching or missing application_id:\n{msg}")


if __name__ == "__main__":
    unittest.main()

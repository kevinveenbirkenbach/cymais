import unittest
import yaml
from pathlib import Path
import re

class TestDockerRoleImagesConfiguration(unittest.TestCase):
    def test_images_keys_and_templates(self):
        """
        For each docker-* role, check that:
        - roles/docker-*/vars/configuration.yml contains 'images' as a dict with keys/values
        - Each image key is referenced as:
            image: "{{ applications[application_id].images.<key> }}"
          in either roles/docker-*/templates/docker-compose.yml.j2 or env.j2
        """
        repo_root = Path(__file__).resolve().parent.parent.parent
        roles_dir = repo_root / "roles"
        errors = []
        warnings = []

        for role_path in roles_dir.iterdir():
            if not (role_path.is_dir() and role_path.name.startswith("docker-")):
                continue

            cfg_file = role_path / "vars" / "configuration.yml"
            if not cfg_file.exists():
                continue  # No configuration to check

            try:
                config = yaml.safe_load(cfg_file.read_text("utf-8")) or {}
                main_file = role_path / "vars" / "main.yml"
                main = yaml.safe_load(main_file.read_text("utf-8")) or {}
            except yaml.YAMLError as e:
                errors.append(f"{role_path.name}: YAML parse error: {e}")
                continue

            images = config.get("images")
            if not images:
                warnings.append(f"[WARNING] {role_path.name}: No 'images' key in configuration.yml")
                continue

            if not isinstance(images, dict):
                errors.append(f"{role_path.name}: 'images' must be a dict in configuration.yml")
                continue

            for key, value in images.items():
                if not key or not value or not isinstance(key, str) or not isinstance(value, str):
                    errors.append(f"{role_path.name}: images['{key}'] is invalid (must be non-empty string key and value)")
                    continue

                # Improved regex: matches both ' and " and allows whitespace
                pattern = (
                    r'image:\s*["\']\{\{\s*applications\[application_id\]\.images\.' + re.escape(key) + r'\s*\}\}["\']'
                )

                # innerhalb Deines Loops
                pattern2 = (
                    r'image:\s*["\']\{\{\s*'                          # image: "{{
                    r'applications\[\s*application_id\s*\]\.images'   # applications[ application_id ].images
                    r'\[\s*application_id\s*\]\s*'                    # [ application_id ]
                    r'\}\}["\']'                                      # }}" oder }}"
                )


                for tmpl_file in [
                    role_path / "templates" / "docker-compose.yml.j2",
                    role_path / "templates" / "env.j2",
                ]:
                    if not tmpl_file.exists():
                        continue
                    content = tmpl_file.read_text("utf-8")
                    if re.search(pattern, content):
                        break
                    if key == main.get('application_id') and re.search(pattern2, content):
                        break
                else:
                    # Dieser Block wird nur ausgeführt, wenn kein `break` ausgelöst wurde
                    errors.append(
                        f"{role_path.name}: image key '{key}' is not referenced as "
                        f"image: \"{{{{ applications[application_id].images.{key} }}}}\" or "
                        f"\"{{{{ applications[application_id].images[application_id] }}}}\" "
                        "in docker-compose.yml.j2 or env.j2"
                    )


                # OPTIONAL: Check if the image is available locally via docker images
                # from shutil import which
                # import subprocess
                # if which("docker"):
                #     try:
                #         out = subprocess.check_output(
                #             ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"]
                #         ).decode()
                #         if value not in out:
                #             errors.append(f"{role_path.name}: Image '{value}' not found locally (optional check)")
                #     except Exception as e:
                #         errors.append(f"{role_path.name}: Error running 'docker images' (optional): {e}")
        if warnings:
            print("\nWarnings in docker role images configuration:\n" + "\n".join(warnings))
        if errors:
            self.fail("Errors in docker role images configuration:\n" + "\n".join(errors))

if __name__ == "__main__":
    unittest.main()

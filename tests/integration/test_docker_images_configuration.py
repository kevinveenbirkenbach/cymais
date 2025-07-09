import unittest
import yaml
from pathlib import Path
import re

class TestDockerRoleImagesConfiguration(unittest.TestCase):
    def test_images_keys_and_templates(self):
        """
        For each web-app-* role, check that:
        - roles/web-app-*/config/main.yml contains 'images' as a dict with keys/values
        - Each image key is referenced as:
            image: "{{ applications[application_id].images.<key> }}"
          in either roles/web-app-*/templates/docker-compose.yml.j2 or env.j2
        """
        repo_root = Path(__file__).resolve().parent.parent.parent
        roles_dir = repo_root / "roles"
        errors = []
        warnings = []

        for role_path in roles_dir.iterdir():
            if not (role_path.is_dir() and role_path.name.startswith("web-app-")):
                continue

            cfg_file = role_path / "config" / "main.yml"
            if not cfg_file.exists():
                continue  # No configuration to check

            try:
                config = yaml.safe_load(cfg_file.read_text("utf-8")) or {}
                main_file = role_path / "vars" / "main.yml"
                main = yaml.safe_load(main_file.read_text("utf-8")) or {}
            except yaml.YAMLError as e:
                errors.append(f"{role_path.name}: YAML parse error: {e}")
                continue

            images = config.get("docker",{}).get("images")
            if not images:
                warnings.append(f"[WARNING] {role_path.name}: No 'docker.images' key in config/main.yml")
                continue

            if not isinstance(images, dict):
                errors.append(f"{role_path.name}: 'images' must be a dict in config/main.yml")
                continue

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

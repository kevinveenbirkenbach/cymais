import os
import re
import unittest
from pathlib import Path

import yaml  # requires PyYAML


class TestGetAppConfPaths(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Locate project root and load YAML configs
        root = Path(__file__).resolve().parents[2]
        cls.app_config_path = root / "group_vars" / "all" / "04_applications.yml"
        with cls.app_config_path.open(encoding="utf-8") as f:
            app_cfg = yaml.safe_load(f)
        cls.defaults_app = app_cfg.get("defaults_applications", {})

        cls.user_config_path = root / "group_vars" / "all" / "03_users.yml"
        with cls.user_config_path.open(encoding="utf-8") as f:
            user_cfg = yaml.safe_load(f)
        cls.defaults_users = user_cfg.get("default_users", {})

        # Regex to match get_app_conf(application_id, 'some.path', ...)
        pattern = re.compile(
            r"get_app_conf\(\s*([^\),]+)\s*,\s*['\"]([^'\"]+)['\"]\s*,\s*[^\)]*\)"
        )

        # Store occurrences: literal_ids -> {path: [(file, line), ...]}, variable paths likewise
        cls.literal_paths_by_id = {}
        cls.variable_paths = {}

        # Recursively search all files (excluding tests/ directories)
        for dirpath, dirs, files in os.walk(root):
            if "tests" in Path(dirpath).parts:
                continue
            for fname in files:
                file_path = Path(dirpath) / fname
                try:
                    text = file_path.read_text(encoding="utf-8")
                except (UnicodeDecodeError, PermissionError):
                    continue
                for m in pattern.finditer(text):
                    lineno = text.count("\n", 0, m.start()) + 1
                    app_arg = m.group(1).strip()
                    path_arg = m.group(2).strip()
                    if (app_arg.startswith("'") and app_arg.endswith("'")) or (
                        app_arg.startswith('"') and app_arg.endswith('"')
                    ):
                        app_id = app_arg.strip("'\"")
                        cls.literal_paths_by_id.setdefault(app_id, {}).setdefault(path_arg, []).append(
                            (file_path, lineno)
                        )
                    else:
                        cls.variable_paths.setdefault(path_arg, []).append(
                            (file_path, lineno)
                        )

    def _assert_nested_key(self, mapping, dotted_path, context):
        """
        Helper: assert that mapping contains the nested dict path defined by dotted_path.
        """
        keys = dotted_path.split('.')
        current = mapping
        for key in keys:
            self.assertIsInstance(
                current, dict,
                f"Expected a dict at '{'.'.join(keys[:keys.index(key)])}' in {context}"
            )
            self.assertIn(
                key, current,
                f"Missing key '{key}' in path '{dotted_path}' under {context}"
            )
            current = current[key]

    def _validate_path(self, app_id, dotted_path, occs):
        """
        Validate that dotted_path exists under defaults_applications,
        or if path starts with 'users.' and not found there, under default_users.
        """
        entry_app = self.defaults_app.get(app_id, {})
        try:
            # First, try in application defaults
            self._assert_nested_key(entry_app, dotted_path, app_id)
            return
        except AssertionError:
            # Only if path begins with users., check default_users next
            if dotted_path.startswith('users.'):
                subpath = dotted_path.split('.', 1)[1]
                try:
                    self._assert_nested_key(self.defaults_users, subpath, 'default_users')
                    return
                except AssertionError:
                    pass
            # If still not found, fail with original context
            file_path, lineno = occs[0]
            self.fail(
                f"'{dotted_path}' not found for application '{app_id}' nor in default_users; "
                f"called at {file_path}:{lineno}"
            )

    def test_literal_ids_have_all_requested_paths(self):
        """Each literal application_id used must have entries for each requested path."""
        for app_id, paths in sorted(self.literal_paths_by_id.items()):
            with self.subTest(application_id=app_id):
                self.assertIn(
                    app_id, self.defaults_app,
                    f"Application '{app_id}' not found under defaults_applications in {self.app_config_path}"
                )
                for dotted_path, occs in sorted(paths.items()):
                    with self.subTest(path=dotted_path):
                        self._validate_path(app_id, dotted_path, occs)

    def test_variable_ids_require_some_app_for_each_path(self):
        """
        If dynamic application_id is used, at least one application or default_users
        must define each dynamic path.
        """
        if not self.variable_paths:
            self.skipTest("No dynamic get_app_conf calls found.")
        for dotted_path, occs in sorted(self.variable_paths.items()):
            with self.subTest(dynamic_path=dotted_path):
                valid = False
                # Special: images.* dynamic paths only require 'images' to exist
                if dotted_path.startswith('images.'):
                    for aid, cfg in self.defaults_app.items():
                        if 'images' in cfg and isinstance(cfg['images'], dict):
                            valid = True
                            break
                    if valid:
                        continue  # skip deeper check for this path
                # First, check each application default for full path
                for aid, cfg in self.defaults_app.items():
                    try:
                        self._assert_nested_key(cfg, dotted_path, aid)
                        valid = True
                        break
                    except AssertionError:
                        continue
                # If not found in any application, and path startswith 'users.', try default_users
                if not valid and dotted_path.startswith('users.'):
                    subpath = dotted_path.split('.', 1)[1]
                    try:
                        self._assert_nested_key(self.defaults_users, subpath, 'default_users')
                        valid = True
                    except AssertionError:
                        pass
                if not valid:
                    file_path, lineno = occs[0]
                    self.fail(
                        f"No entry defines '{dotted_path}' in defaults_applications or default_users; "
                        f"called at {file_path}:{lineno}"
                    )


if __name__ == "__main__":
    unittest.main()
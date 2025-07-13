import os
import re
import unittest
from pathlib import Path

import yaml  # requires PyYAML
# Import the get_role filter directly
from filter_plugins.get_role import get_role


class TestGetAppConfPaths(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Locate project root and load YAML configs
        root = Path(__file__).resolve().parents[2]
        cls.root = root
        cls.app_config_path = root / "group_vars" / "all" / "04_applications.yml"
        with cls.app_config_path.open(encoding="utf-8") as f:
            app_cfg = yaml.safe_load(f)
        cls.defaults_app = app_cfg.get("defaults_applications", {})

        cls.user_config_path = root / "group_vars" / "all" / "03_users.yml"
        with cls.user_config_path.open(encoding="utf-8") as f:
            user_cfg = yaml.safe_load(f)
        cls.defaults_users = user_cfg.get("default_users", {})

        # Regex to match get_app_conf(application_id, 'some.path', ...)
        cls.pattern = re.compile(
            r"get_app_conf\(\s*([^\),]+)\s*,\s*['\"]([^'\"]+)['\"]\s*,\s*[^\)]*\)"
        )

        # Store occurrences: literal_ids -> {path: [(file, line), ...]}, variable paths likewise
        cls.literal_paths_by_id = {}
        cls.variable_paths = {}

        # Scan all files except tests/
        for dirpath, dirs, files in os.walk(root):
            if "tests" in Path(dirpath).parts:
                continue
            for fname in files:
                file_path = Path(dirpath) / fname
                try:
                    text = file_path.read_text(encoding="utf-8")
                except (UnicodeDecodeError, PermissionError):
                    continue
                for m in cls.pattern.finditer(text):
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
        keys = dotted_path.split('.')
        current = mapping
        for key in keys:
            self.assertIsInstance(current, dict,
                f"Expected dict at '{'.'.join(keys[:keys.index(key)])}' in {context}")
            self.assertIn(key, current,
                f"Missing '{key}' in path '{dotted_path}' under {context}")
            current = current[key]

    def _validate_credentials(self, application_id, key, occs):
        # Delegate to get_role filter to find role name
        role = get_role(application_id, roles_path=str(self.root / 'roles'))
        schema_file = self.root / 'roles' / role / 'schema' / 'main.yml'
        self.assertTrue(schema_file.is_file(), f"Schema file not found: {schema_file}")
        with schema_file.open(encoding="utf-8") as sf:
            schema = yaml.safe_load(sf) or {}
        creds = schema.get('credentials')
        self.assertIsInstance(creds, dict,
            f"'credentials' missing or not dict in {schema_file}")
        self.assertIn(key, creds,
            f"Missing credential '{key}' in {schema_file} for role '{role}'")

    def _validate_path(self, app_id, dotted_path, occs):
        entry_app = self.defaults_app.get(app_id, {})
        try:
            self._assert_nested_key(entry_app, dotted_path, app_id)
            return
        except AssertionError:
            # users.* fallback
            if dotted_path.startswith('users.'):
                subpath = dotted_path.split('.', 1)[1]
                try:
                    self._assert_nested_key(self.defaults_users, subpath, 'default_users')
                    return
                except AssertionError:
                    pass
            # credentials.* fallback via get_role
            if dotted_path.startswith('credentials.'):
                key = dotted_path.split('.', 1)[1]
                self._validate_credentials(app_id, key, occs)
                return
            # images.* only require top-level images dict
            if dotted_path.startswith('images.'):
                if any('images' in cfg and isinstance(cfg['images'], dict)
                       for cfg in self.defaults_app.values()):
                    return
            file_path, lineno = occs[0]
            self.fail(f"'{dotted_path}' not found for '{app_id}'; called at {file_path}:{lineno}")

    def test_literal_paths(self):
        for app_id, paths in sorted(self.literal_paths_by_id.items()):
            with self.subTest(app_id=app_id):
                self.assertIn(app_id, self.defaults_app,
                    f"App '{app_id}' not in defaults_applications")
                for dotted_path, occs in sorted(paths.items()):
                    with self.subTest(path=dotted_path):
                        self._validate_path(app_id, dotted_path, occs)

    def test_variable_paths(self):
        if not self.variable_paths:
            self.skipTest("No dynamic calls found.")
        for dotted_path, occs in sorted(self.variable_paths.items()):
            with self.subTest(path=dotted_path):
                valid = False
                # credentials.* dynamic
                if dotted_path.startswith('credentials.'):
                    key = dotted_path.split('.',1)[1]
                    for aid in self.defaults_app:
                        try:
                            self._validate_credentials(aid, key, occs)
                            valid = True; break
                        except AssertionError:
                            pass
                    if valid: continue
                # images.* dynamic
                if dotted_path.startswith('images.'):
                    if any('images' in cfg and isinstance(cfg['images'], dict)
                           for cfg in self.defaults_app.values()):
                        continue
                # check app defaults
                for aid, cfg in self.defaults_app.items():
                    try:
                        self._assert_nested_key(cfg, dotted_path, aid)
                        valid = True; break
                    except AssertionError:
                        pass
                # users.* fallback
                if not valid and dotted_path.startswith('users.'):
                    subpath = dotted_path.split('.',1)[1]
                    try:
                        self._assert_nested_key(self.defaults_users, subpath, 'default_users')
                        valid = True
                    except AssertionError:
                        pass
                if not valid:
                    file_path, lineno = occs[0]
                    self.fail(f"No entry for '{dotted_path}'; called at {file_path}:{lineno}")


if __name__ == "__main__":
    unittest.main()

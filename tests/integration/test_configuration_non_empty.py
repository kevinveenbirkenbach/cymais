import os
import glob
import yaml
import unittest


def find_none_values(data, prefix=None):
    """
    Recursively find keys with None values in a nested dict or list.
    Returns a list of (path, value) tuples where value is None.
    """
    errors = []
    if prefix is None:
        prefix = []

    if isinstance(data, dict):
        for key, value in data.items():
            path = prefix + [str(key)]
            if value is None:
                errors.append((".".join(path), value))
            elif isinstance(value, (dict, list)):
                errors.extend(find_none_values(value, path))
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            path = prefix + [f"[{idx}]"]
            if item is None:
                errors.append((".".join(path), item))
            elif isinstance(item, (dict, list)):
                errors.extend(find_none_values(item, path))

    return errors


class TestConfigurationNoNone(unittest.TestCase):
    def test_configuration_files_have_no_none_values(self):
        # Find all configuration.yml files under roles/*/vars
        pattern = os.path.join(
            os.path.dirname(__file__),
            os.pardir, os.pardir,
            'roles', '*', 'vars', 'configuration.yml'
        )
        files = glob.glob(pattern)
        self.assertTrue(files, f"No configuration.yml files found with pattern: {pattern}")

        all_errors = []
        for filepath in files:
            with open(filepath, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    self.fail(f"Failed to parse YAML in {filepath}: {e}")
            errors = find_none_values(data)
            for path, value in errors:
                all_errors.append(f"{filepath}: Key '{path}' is None")

        if all_errors:
            self.fail("None values found in configuration files:\n" + "\n".join(all_errors))


if __name__ == '__main__':
    unittest.main()

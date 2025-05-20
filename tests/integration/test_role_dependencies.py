import unittest
import os
import yaml
import warnings

def load_yaml_file(file_path):
    """Load a YAML file and return its content."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file) or {}

def get_meta_info(role_path):
    """Extract dependencies and run orders (before/after) from the meta/main.yml of a role."""
    meta_file = os.path.join(role_path, 'meta', 'main.yml')
    if not os.path.isfile(meta_file):
        return [], [], []
    meta_data = load_yaml_file(meta_file)
    dependencies = meta_data.get('dependencies', [])
    run_order = meta_data.get('applications_run_order', {})
    return dependencies, run_order.get('before', []), run_order.get('after', [])

def resolve_dependencies(roles_dir):
    """Resolve all role dependencies and detect circular dependencies."""
    visited = set()
    stack = set()

    def visit(role_path):
        role_name = os.path.basename(role_path)

        # Check for circular dependencies
        if role_name in stack:
            warning_msg = f"Circular dependency detected with role: {role_name} in path: {' -> '.join(stack)}"
            warnings.warn(warning_msg)
            raise ValueError(f"Circular dependency detected with role: {role_name} in path: {' -> '.join(stack)}")

        # Check if role is already processed
        if role_name in visited:
            return [], []

        # Mark role as being processed
        stack.add(role_name)
        visited.add(role_name)

        # Get dependencies and before/after orders
        dependencies, before, after = get_meta_info(role_path)

        # Resolve before dependencies
        before_order, after_order = [], []
        for dep in dependencies:
            # Add more detailed debug information for `dep`
            try:
                print(f"Visiting dependency: {dep} for role {role_name}, role_path: {role_path}")
                # Check if dep is a dictionary and extract the role name if necessary
                if isinstance(dep, dict):
                    print(f"Dependency {dep} is a dictionary. Extracting role name...")
                    dep = list(dep.keys())[0]  # Extract the key if it's a dictionary
                dep_path = os.path.join(roles_dir, dep)
                print(f"Resolved dependency path: {dep_path}")

                dep_before, dep_after = visit(dep_path)  # Recurse into dependencies
                before_order.extend(dep_before)
                after_order.extend(dep_after)
            except Exception as e:
                # Print error message with role path to help with debugging
                raise ValueError(f"Error in role {role_name} while processing dependency {dep} at path {role_path}: {str(e)}")

        # Add the current role's own before/after orders
        before_order.extend(before)
        after_order.extend(after)

        # Mark role as processed
        stack.remove(role_name)

        return before_order, after_order

    all_run_orders = {}

    for role_name in os.listdir(roles_dir):
        role_path = os.path.join(roles_dir, role_name)
        if os.path.isdir(role_path):
            try:
                all_run_orders[role_path] = visit(role_path)
            except ValueError as e:
                # Improved error reporting with role path information
                raise ValueError(f"Error processing role '{role_name}' at path '{role_path}': {str(e)}")

    return all_run_orders


class TestRoleDependencies(unittest.TestCase):
    def test_no_circular_dependencies(self):
        roles_dir = "roles"
        try:
            run_orders = resolve_dependencies(roles_dir)
        except ValueError as e:
            self.fail(f"Circular dependency detected: {e}")

        # If no exception, the test passed
        self.assertIsInstance(run_orders, dict)

if __name__ == '__main__':
    unittest.main()

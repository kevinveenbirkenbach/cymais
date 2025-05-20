import unittest
import os
import yaml

def load_yaml_file(file_path):
    """Load a YAML file and return its content."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file) or {}

def get_meta_info(role_path):
    """Extract before and after dependencies from the meta/main.yml of a role."""
    meta_file = os.path.join(role_path, 'meta', 'main.yml')
    if not os.path.isfile(meta_file):
        return [], []
    meta_data = load_yaml_file(meta_file)
    run_order = meta_data.get('role_run_order', {})
    before = run_order.get('before', [])
    after = run_order.get('after', [])
    return before, after

def resolve_dependencies(roles_dir):
    """Resolve all role dependencies and detect circular dependencies in before/after."""
    visited = set()  # Tracks roles that have been processed
    stack = set()  # Tracks roles being processed in the current recursion path

    def visit(role_path, stack):
        role_name = os.path.basename(role_path)

        # Check for circular dependencies in the recursion path (for before/after)
        if role_name in stack:
            raise ValueError(f"Circular dependency detected in 'before'/'after' between roles: {' -> '.join(stack)} -> {role_name}")

        # Check if role is already processed
        if role_name in visited:
            return []

        # Mark role as visited and add to stack
        visited.add(role_name)
        stack.append(role_name)

        # Get before and after dependencies
        before, after = get_meta_info(role_path)

        # Resolve before and after roles
        for before_role in before:
            before_role_path = os.path.join(roles_dir, before_role)
            visit(before_role_path, stack)  # Recurse into before dependencies

        for after_role in after:
            after_role_path = os.path.join(roles_dir, after_role)
            visit(after_role_path, stack)  # Recurse into after dependencies

        stack.pop()  # Remove the current role from the stack

    for role_name in os.listdir(roles_dir):
        role_path = os.path.join(roles_dir, role_name)
        if os.path.isdir(role_path):
            try:
                visit(role_path, [])  # Start recursion from this role
            except ValueError as e:
                raise ValueError(f"Error processing role '{role_name}' at path '{role_path}': {str(e)}")

    return "No Circular Dependency Detected"

class TestRoleBeforeAfterDependencies(unittest.TestCase):
    def test_no_circular_before_after_dependencies(self):
        roles_dir = "roles"  # Path to the roles directory

        try:
            result = resolve_dependencies(roles_dir)
        except ValueError as e:
            self.fail(f"Circular dependency detected: {e}")

        # If no exception, the test passed
        self.assertEqual(result, "No Circular Dependency Detected")

if __name__ == '__main__':
    unittest.main()

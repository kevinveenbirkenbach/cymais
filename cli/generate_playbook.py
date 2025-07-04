import os
import yaml
import argparse
from collections import defaultdict, deque

def find_roles(roles_dir, prefix=None):
    """Find all roles in the given directory."""
    for entry in os.listdir(roles_dir):
        if prefix and not entry.startswith(prefix):
            continue
        path = os.path.join(roles_dir, entry)
        meta_file = os.path.join(path, 'meta', 'main.yml')
        if os.path.isdir(path) and os.path.isfile(meta_file):
            yield path, meta_file

def load_run_after(meta_file):
    """Load the 'run_after' from the meta/main.yml of a role."""
    with open(meta_file, 'r') as f:
        data = yaml.safe_load(f) or {}
    return data.get('galaxy_info', {}).get('run_after', [])

def load_application_id(role_path):
    """Load the application_id from the vars/main.yml of the role."""
    vars_file = os.path.join(role_path, 'vars', 'main.yml')
    if os.path.exists(vars_file):
        with open(vars_file, 'r') as f:
            data = yaml.safe_load(f) or {}
        return data.get('application_id')
    return None

def build_dependency_graph(roles_dir, prefix=None):
    """Build a dependency graph where each role points to the roles it depends on."""
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    roles = {}

    for role_path, meta_file in find_roles(roles_dir, prefix):
        run_after = load_run_after(meta_file)
        application_id = load_application_id(role_path)
        role_name = os.path.basename(role_path)
        roles[role_name] = {
            'role_name': role_name,
            'run_after': run_after,
            'application_id': application_id,
            'path': role_path
        }

        # If the role has dependencies, build the graph
        for dependency in run_after:
            graph[dependency].append(role_name)
            in_degree[role_name] += 1

        # Ensure roles with no dependencies have an in-degree of 0
        if role_name not in in_degree:
            in_degree[role_name] = 0

    return graph, in_degree, roles

def topological_sort(graph, in_degree):
    """Perform topological sort on the dependency graph."""
    # Queue for roles with no incoming dependencies (in_degree == 0)
    queue = deque([role for role, degree in in_degree.items() if degree == 0])
    sorted_roles = []

    while queue:
        role = queue.popleft()
        sorted_roles.append(role)

        # Reduce in-degree for roles dependent on the current role
        for neighbor in graph[role]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_roles) != len(in_degree):
        # If the number of sorted roles doesn't match the number of roles,
        # there was a cycle in the graph (not all roles could be sorted)
        raise Exception("Circular dependency detected among the roles!")

    return sorted_roles

def print_dependency_tree(graph):
    """Print the dependency tree visually on the console."""
    def print_node(role, indent=0):
        print("  " * indent + role)
        for dependency in graph[role]:
            print_node(dependency, indent + 1)

    # Print the tree starting from roles with no dependencies
    all_roles = set(graph.keys())
    dependent_roles = {role for dependencies in graph.values() for role in dependencies}
    root_roles = all_roles - dependent_roles

    printed_roles = []

    def collect_roles(role, indent=0):
        printed_roles.append(role)
        for dependency in graph[role]:
            collect_roles(dependency, indent + 1)

    for root in root_roles:
        collect_roles(root)

    return printed_roles

def generate_playbook_entries(roles_dir, prefix=None):
    """Generate playbook entries based on the sorted order."""
    graph, in_degree, roles = build_dependency_graph(roles_dir, prefix)

    # Detect cycles and get correct topological order
    sorted_role_names = topological_sort(graph, in_degree)

    entries = []
    for role_name in sorted_role_names:
        role = roles[role_name]
        entries.append(
            f"- name: setup {role['application_id']}\n"
            f"  when: {role['application_id']} | application_allowed(group_names, allowed_applications)\n"
            f"  include_role:\n"
            f"    name: {role['role_name']}\n"
        )
        entries.append(
            f"- name: flush handlers after {role['application_id']}\n"
            f"  meta: flush_handlers\n"
        )

    return entries

def main():
    parser = argparse.ArgumentParser(
        description='Generate an Ansible playbook include file from Docker roles, sorted by run_after order.'
    )
    parser.add_argument(
        'roles_dir',
        help='Path to directory containing role folders'
    )
    parser.add_argument(
        '-p', '--prefix',
        help='Only include roles whose names start with this prefix (e.g. docker-, client-)',
        default=None
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)',
        default=None
    )
    parser.add_argument(
        '-t', '--tree',
        action='store_true',
        help='Display the dependency tree of roles visually'
    )
    args = parser.parse_args()

    # Generate and output the playbook entries
    entries = generate_playbook_entries(args.roles_dir, args.prefix)
    output = ''.join(entries)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Playbook entries written to {args.output}")
    else:
        print(output)

if __name__ == '__main__':
    main()

import os
import argparse
import yaml


def find_roles(roles_dir, prefix=None):
    """
    Yield absolute paths of role directories under roles_dir.
    Only include roles whose directory name starts with prefix (if given) and contain meta/main.yml.
    """
    for entry in os.listdir(roles_dir):
        if prefix and not entry.startswith(prefix):
            continue
        path = os.path.join(roles_dir, entry)
        meta_file = os.path.join(path, 'meta', 'main.yml')
        if os.path.isdir(path) and os.path.isfile(meta_file):
            yield path, meta_file


def load_role_order(meta_file):
    """
    Load the meta/main.yml and return the role_run_order field.
    Returns a dict with 'before' and 'after' keys. Defaults to empty lists if not found.
    """
    with open(meta_file, 'r') as f:
        data = yaml.safe_load(f) or {}
    run_order = data.get('role_run_order', {})
    before = run_order.get('before', [])
    after = run_order.get('after', [])
    
    # If "all" is in before or after, treat it as a special value
    if "all" in before:
        before.remove("all")
        before.insert(0, "all")  # Treat "all" as the first item
    if "all" in after:
        after.remove("all")
        after.append("all")  # Treat "all" as the last item
    
    return {
        'before': before,
        'after': after
    }


def sort_roles_by_order(roles_dir, prefix=None):
    roles = []
    
    # Collect roles and their before/after dependencies
    for role_path, meta_file in find_roles(roles_dir, prefix):
        run_order = load_role_order(meta_file)
        role_name = os.path.basename(role_path)
        roles.append({
            'role_name': role_name,
            'before': run_order['before'],
            'after': run_order['after'],
            'path': role_path
        })

    # Now sort the roles based on before/after relationships
    sorted_roles = []
    unresolved_roles = roles[:]
    
    # First, place roles with "before: all" at the start
    roles_with_before_all = [role for role in unresolved_roles if "all" in role['before']]
    sorted_roles.extend(roles_with_before_all)
    unresolved_roles = [role for role in unresolved_roles if "all" not in role['before']]
    
    while unresolved_roles:
        # Find roles with no dependencies in 'before'
        ready_roles = [role for role in unresolved_roles if not any(dep in [r['role_name'] for r in unresolved_roles] for dep in role['before'])]
        
        if not ready_roles:
            raise ValueError("Circular dependency detected in 'before'/'after' fields")

        for role in ready_roles:
            sorted_roles.append(role)
            unresolved_roles.remove(role)

            # Remove from the 'before' lists of remaining roles
            for r in unresolved_roles:
                r['before'] = [dep for dep in r['before'] if dep != role['role_name']]

    # Finally, place roles with "after: all" at the end
    roles_with_after_all = [role for role in unresolved_roles if "all" in role['after']]
    sorted_roles.extend(roles_with_after_all)
    unresolved_roles = [role for role in unresolved_roles if "all" not in role['after']]

    return sorted_roles


def generate_playbook_entries(roles_dir, prefix=None):
    entries = []
    sorted_roles = sort_roles_by_order(roles_dir, prefix)

    for role in sorted_roles:
        # entry text
        entry = (
            f"- name: setup {role['role_name']}\n"
            f"  when: (\"{role['role_name']}\" in group_names)\n"
            f"  include_role:\n"
            f"    name: {role['role_name']}\n"
        )
        entries.append(entry)

    return entries


def main():
    parser = argparse.ArgumentParser(
        description='Generate an Ansible playbook include file from Docker roles and application_ids, sorted by role_run_order.'
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
    args = parser.parse_args()

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

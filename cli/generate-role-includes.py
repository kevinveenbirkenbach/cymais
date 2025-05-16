import os
import argparse
import yaml

def find_roles(roles_dir, prefix=None):
    """
    Yield absolute paths of role directories under roles_dir.
    Only include roles whose directory name starts with prefix (if given) and contain vars/main.yml.
    """
    for entry in os.listdir(roles_dir):
        if prefix and not entry.startswith(prefix):
            continue
        path = os.path.join(roles_dir, entry)
        vars_file = os.path.join(path, 'vars', 'main.yml')
        if os.path.isdir(path) and os.path.isfile(vars_file):
            yield path, vars_file


def load_application_id(vars_file):
    """
    Load the vars/main.yml and return the value of application_id key.
    Returns None if not found.
    """
    with open(vars_file, 'r') as f:
        data = yaml.safe_load(f) or {}
    return data.get('application_id')


def generate_playbook_entries(roles_dir, prefix=None):
    entries = []
    for role_path, vars_file in find_roles(roles_dir, prefix):
        app_id = load_application_id(vars_file)
        if not app_id:
            continue
        # Derive role name from directory name
        role_name = os.path.basename(role_path)
        # entry text
        entry = (
            f"- name: setup {app_id}\n"
            f"  when: (\"{app_id}\" in group_names)\n"
            f"  include_role:\n"
            f"    name: {role_name}\n"
        )
        entries.append(entry)
    return entries


def main():
    parser = argparse.ArgumentParser(
        description='Generate an Ansible playbook include file from Docker roles and application_ids.'
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
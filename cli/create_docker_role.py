#!/usr/bin/env python3
import argparse
import os
import shutil
import sys
import yaml
import ipaddress
import difflib
from jinja2 import Environment, FileSystemLoader

# Paths to the group-vars files
PORTS_FILE = './group_vars/all/09_ports.yml'
NETWORKS_FILE = './group_vars/all/10_networks.yml'
ROLE_TEMPLATE_DIR = './templates/docker_role'
ROLES_DIR = './roles'


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def dump_yaml(data, path):
    with open(path, 'w') as f:
        yaml.safe_dump(data, f, sort_keys=False)


def get_next_network(networks_dict, prefixlen):
    """Select the first available local subnet with the given prefix length."""
    nets = []
    for info in networks_dict['defaults_networks']['local'].values():
        net = ipaddress.ip_network(info['subnet'])
        if net.prefixlen == prefixlen:
            nets.append(net)
    nets.sort(key=lambda n: int(n.network_address))
    return nets[0]


def get_next_port(ports_dict, category):
    """Find the next unused port in the given localhost category."""
    used = {int(p) for p in ports_dict['ports']['localhost'].get(category, {}).values()}
    candidate = 1
    while candidate in used:
        candidate += 1
    return candidate


def prompt_conflict(dst_file):
    """Prompt the user to resolve a file conflict."""
    print(f"Conflict detected: {dst_file}")
    print("Choose action: [1] overwrite, [2] skip, [3] merge")
    choice = None
    while choice not in ('1', '2', '3'):
        choice = input("Enter 1, 2, or 3: ").strip()
    return choice


def render_template(src_dir, dst_dir, context):
    """Recursively render all templates from src_dir into dst_dir, handling conflicts."""
    env = Environment(
        loader=FileSystemLoader(src_dir),
        keep_trailing_newline=True,
        autoescape=False,
    )
    # Add a bool filter for Jinja evaluation
    env.filters['bool'] = lambda x: bool(x)
    for root, _, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        target_path = os.path.join(dst_dir, rel_path)
        os.makedirs(target_path, exist_ok=True)
        for filename in files:
            template = env.get_template(os.path.join(rel_path, filename))
            rendered = template.render(**context)
            out_name = filename[:-3] if filename.endswith('.j2') else filename
            dst_file = os.path.join(target_path, out_name)

            if os.path.exists(dst_file):
                choice = prompt_conflict(dst_file)
                if choice == '2':
                    print(f"Skipping {dst_file}")
                    continue
                if choice == '3':
                    with open(dst_file) as f_old:
                        old_lines = f_old.readlines()
                    new_lines = rendered.splitlines(keepends=True)
                    diff = difflib.unified_diff(
                        old_lines, new_lines,
                        fromfile=f"a/{out_name}",
                        tofile=f"b/{out_name}",
                        lineterm=''
                    )
                    diff_path = dst_file + '.diff'
                    with open(diff_path, 'w') as fd:
                        fd.writelines(diff)
                    print(f"Diff written to {diff_path}; please merge manually.")
                    continue
                # Overwrite
                print(f"Overwriting {dst_file}")

            with open(dst_file, 'w') as f:
                f.write(rendered)


def main():
    # Load current port categories dynamically
    ports_yaml = load_yaml(PORTS_FILE)
    categories = list(ports_yaml.get('ports', {}).get('localhost', {}).keys())

    parser = argparse.ArgumentParser(
        description="Create or update a Docker Ansible role, and assign network and ports"
    )
    parser.add_argument(
        '-a', '--application-id', required=True,
        help="Unique application ID"
    )
    parser.add_argument(
        '-n', '--network', choices=['24', '28'], required=True,
        help="Network prefix length (/24 or /28)"
    )
    parser.add_argument(
        '-p', '--ports', nargs='+', choices=categories, required=True,
        help=f"Port categories to assign (allowed: {', '.join(categories)})"
    )
    args = parser.parse_args()

    app_id = args.application_id
    role_name = f"docker-{app_id}"
    role_dir = os.path.join(ROLES_DIR, role_name)

    # If role directory exists, ask whether to continue
    if os.path.exists(role_dir):
        cont = input(f"Role {role_name} already exists. Continue updating? [y/N]: ").strip().lower()
        if cont != 'y':
            print("Aborting.")
            sys.exit(1)
    else:
        os.makedirs(role_dir)

    # 1) Render and copy templates, with conflict resolution
    # Provide database_type=0 in context for task template logic
    render_template(ROLE_TEMPLATE_DIR, role_dir, {
        'application_id': app_id,
        'role_name': role_name,
        'database_type': 0,
    })
    print(f"→ Templates rendered into {role_dir}")

    # 2) Assign network if not already set
    net_vars_file = f'./group_vars/{app_id}_network.yml'
    if os.path.exists(net_vars_file):
        existing_net = load_yaml(net_vars_file)
        apps = existing_net.get('defaults_networks', {}).get('application', {})
        if app_id in apps:
            print(f"→ Network for {app_id} already configured ({apps[app_id]}), skipping.")
        else:
            networks = load_yaml(NETWORKS_FILE)
            net = get_next_network(networks, int(args.network))
            apps[app_id] = str(net)
            dump_yaml(existing_net, net_vars_file)
            print(f"→ Appended network {net} for {app_id}")
    else:
        networks = load_yaml(NETWORKS_FILE)
        net = get_next_network(networks, int(args.network))
        dump_yaml({'defaults_networks': {'application': {app_id: str(net)}}}, net_vars_file)
        print(f"→ Created network vars file with {net} for {app_id}")

    # 3) Assign ports if not present
    assigned = {}
    for cat in args.ports:
        loc = ports_yaml['ports']['localhost'].setdefault(cat, {})
        if app_id in loc:
            print(f"→ Port for category '{cat}' and '{app_id}' already exists ({loc[app_id]}), skipping.")
            continue
        port = get_next_port(ports_yaml, cat)
        loc[app_id] = port
        assigned[cat] = port

    if assigned:
        shutil.copy(PORTS_FILE, PORTS_FILE + '.bak')
        dump_yaml(ports_yaml, PORTS_FILE)
        print(f"→ Assigned new ports: {assigned}")
    else:
        print("→ No new ports to assign, skipping update of 09_ports.yml.")

    # 4) Write or merge application-specific ports file
    app_ports_file = f'./group_vars/{app_id}_ports.yml'
    if os.path.exists(app_ports_file):
        app_ports = load_yaml(app_ports_file)
        dest = app_ports.setdefault('ports', {}).setdefault('localhost', {})
        for cat, port in assigned.items():
            dest[cat] = port
        dump_yaml(app_ports, app_ports_file)
    else:
        dump_yaml({'ports': {'localhost': assigned}}, app_ports_file)
    print(f"→ App-specific ports written to {app_ports_file}")


if __name__ == '__main__':
    main()

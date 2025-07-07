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
    """Select the next contiguous subnet by taking the highest existing subnet and adding one network-size offset."""
    nets = []
    for info in networks_dict['defaults_networks']['local'].values():
        net = ipaddress.ip_network(info['subnet'])
        if net.prefixlen == prefixlen:
            nets.append(net)
    if not nets:
        raise RuntimeError(f"No existing /{prefixlen} networks to base allocation on.")
    nets.sort(key=lambda n: int(n.network_address))
    last = nets[-1]
    offset = last.num_addresses
    next_network_address = int(last.network_address) + offset
    return ipaddress.ip_network((next_network_address, prefixlen))


def get_next_port(ports_dict, category):
    """Assign the next port by taking max existing and adding one."""
    existing = [int(p) for p in ports_dict['ports']['localhost'].get(category, {}).values()]
    return (max(existing) + 1) if existing else 1


def prompt_conflict(dst_file):
    """Prompt the user to resolve a file conflict."""
    print(f"Conflict detected: {dst_file}")
    print("Choose action: [1] overwrite, [2] skip, [3] merge")
    choice = None
    while choice not in ('1', '2', '3'):
        choice = input("Enter 1, 2, or 3: ").strip()
    return choice


def render_templates(src_dir, dst_dir, context):
    """Recursively render all templates from src_dir into dst_dir, handling conflicts."""
    env = Environment(
        loader=FileSystemLoader(src_dir),
        keep_trailing_newline=True,
        autoescape=False,
    )
    env.filters['bool'] = lambda x: bool(x)

    for root, _, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        target = os.path.join(dst_dir, rel)
        os.makedirs(target, exist_ok=True)
        for fn in files:
            tpl = env.get_template(os.path.join(rel, fn))
            rendered = tpl.render(**context)
            out_name = fn[:-3] if fn.endswith('.j2') else fn
            dst_file = os.path.join(target, out_name)

            if os.path.exists(dst_file):
                choice = prompt_conflict(dst_file)
                if choice == '2':  # skip
                    print(f"Skipping {dst_file}")
                    continue
                if choice == '3':  # merge: append lines not present
                    with open(dst_file) as f_old:
                        old = f_old.readlines()
                    new = rendered.splitlines(keepends=True)
                    add = [l for l in new if l not in old]
                    if add:
                        with open(dst_file, 'a') as f:
                            f.writelines(add)
                        print(f"Merged {len(add)} new lines into {dst_file}")
                    else:
                        print(f"Nothing new to merge in {dst_file}")
                    continue
                # overwrite
                print(f"Overwriting {dst_file}")
                with open(dst_file, 'w') as f:
                    f.write(rendered)
            else:
                # new file
                with open(dst_file, 'w') as f:
                    f.write(rendered)


def main():
    # load dynamic port categories
    ports_yaml = load_yaml(PORTS_FILE)
    categories = list(ports_yaml.get('ports', {}).get('localhost', {}).keys())

    parser = argparse.ArgumentParser(
        description="Create or update a Docker Ansible role, assign network and ports globally"
    )
    parser.add_argument('-a', '--application-id', required=True, help="Unique application ID")
    parser.add_argument('-n', '--network', choices=['24', '28'], required=True,
                        help="Network prefix length (/24 or /28)")
    parser.add_argument('-p', '--ports', nargs='+', choices=categories, required=True,
                        help=f"Port categories to assign (allowed: {', '.join(categories)})")
    args = parser.parse_args()

    app = args.application_id
    role = f"docker-{app}"
    role_dir = os.path.join(ROLES_DIR, role)

    # ensure role dir exists, prompt if updating
    if os.path.exists(role_dir):
        if input(f"Role {role} exists. Continue update? [y/N]: ").strip().lower() != 'y':
            print("Aborted.")
            sys.exit(1)
    else:
        os.makedirs(role_dir)

    # 1) render templates
    render_templates(ROLE_TEMPLATE_DIR, role_dir, {'application_id': app,
                                                    'role_name': role,
                                                    'database_type': 0})
    print(f"→ Templates applied to {role_dir}")

    # 2) assign and update global networks
    nets = load_yaml(NETWORKS_FILE)
    net = get_next_network(nets, int(args.network))
    nets['defaults_networks']['local'][app] = str(net)
    dump_yaml(nets, NETWORKS_FILE)
    print(f"→ Assigned network {net} to {app} in {NETWORKS_FILE}")

    # 3) assign and update global ports
    assigned = {}
    for cat in args.ports:
        port = get_next_port(ports_yaml, cat)
        ports_yaml['ports']['localhost'].setdefault(cat, {})[app] = port
        assigned[cat] = port

    if assigned:
        shutil.copy(PORTS_FILE, PORTS_FILE + '.bak')
        dump_yaml(ports_yaml, PORTS_FILE)
        print(f"→ Assigned ports {assigned} for {app} in {PORTS_FILE}")
    else:
        print("→ No ports assigned (already existed)")

if __name__ == '__main__':
    main()

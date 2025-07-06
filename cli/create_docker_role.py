#!/usr/bin/env python3
import argparse
import os
import shutil
import yaml
import ipaddress
from jinja2 import Environment, FileSystemLoader

# Paths to the group-vars files
PORTS_FILE = './group_vars/all/09_ports.yml'
NETWORKS_FILE = './group_vars/all/10_networks.yml'
ROLE_TEMPLATE_DIR = './docker-template'
ROLES_DIR = './roles'


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def dump_yaml(data, path):
    with open(path, 'w') as f:
        yaml.safe_dump(data, f, sort_keys=False)


def get_next_network(networks_dict, prefixlen):
    # Collect all local subnets matching the given prefix length
    nets = []
    for name, info in networks_dict['defaults_networks']['local'].items():
        net = ipaddress.ip_network(info['subnet'])
        if net.prefixlen == prefixlen:
            nets.append(net)
    # Sort by network address and return the first one
    nets.sort(key=lambda n: int(n.network_address))
    return nets[0]


def get_next_port(ports_dict, category, service):
    used = set()
    # Gather already taken ports under localhost.category
    for svc, port in ports_dict['ports']['localhost'].get(category, {}).items():
        used.add(int(port))
    # Start searching from port 1 upwards
    candidate = 1
    while candidate in used:
        candidate += 1
    return candidate


def render_template(src_dir, dst_dir, context):
    env = Environment(
        loader=FileSystemLoader(src_dir),
        keep_trailing_newline=True,
        autoescape=False,
    )
    for root, _, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        target_path = os.path.join(dst_dir, rel_path)
        os.makedirs(target_path, exist_ok=True)
        for filename in files:
            template = env.get_template(os.path.join(rel_path, filename))
            rendered = template.render(**context)
            out_name = filename[:-3] if filename.endswith('.j2') else filename
            with open(os.path.join(target_path, out_name), 'w') as f:
                f.write(rendered)


def main():
    parser = argparse.ArgumentParser(
        description="Create a Docker Ansible role with Jinja2 templates, and assign network and ports"
    )
    parser.add_argument(
        '--application-id', '-a', required=True,
        help="Unique ID of the application (used in the role name)"
    )
    parser.add_argument(
        '--network', '-n', choices=['24', '28'], required=True,
        help="Network prefix length to assign (/24 or /28)"
    )
    parser.add_argument(
        '--ports', '-p', nargs='+', metavar="CATEGORY.SERVICE", required=True,
        help="List of ports in the format category.service (e.g. http.nextcloud)"
    )
    args = parser.parse_args()

    app_id = args.application_id
    role_name = f"docker-{app_id}"

    # 1) Create the role from the template
    role_dir = os.path.join(ROLES_DIR, role_name)
    if os.path.exists(role_dir):
        parser.error(f"Role {role_name} already exists at {role_dir}")
    render_template(ROLE_TEMPLATE_DIR, role_dir, {
        'application_id': app_id,
        'role_name': role_name,
    })
    print(f"→ Role {role_name} created at {role_dir}")

    # 2) Assign network
    networks = load_yaml(NETWORKS_FILE)
    prefix = int(args.network)
    chosen_net = get_next_network(networks, prefix)
    out_net = {
        'defaults_networks': {
            'application': {
                app_id: str(chosen_net)
            }
        }
    }
    net_file = f'./group_vars/{app_id}_network.yml'
    dump_yaml(out_net, net_file)
    print(f"→ Assigned network {chosen_net} (/{prefix}) and wrote to {net_file}")

    # 3) Assign ports
    ports_yaml = load_yaml(PORTS_FILE)
    assigned = {}
    for entry in args.ports:
        try:
            category, service = entry.split('.', 1)
        except ValueError:
            parser.error(f"Invalid port spec: {entry}. Must be CATEGORY.SERVICE")
        port = get_next_port(ports_yaml, category, service)
        # Insert into the in-memory ports data under localhost
        ports_yaml['ports']['localhost'].setdefault(category, {})[service] = port
        assigned[entry] = port

    # Backup and write updated all/09_ports.yml
    backup_file = PORTS_FILE + '.bak'
    shutil.copy(PORTS_FILE, backup_file)
    dump_yaml(ports_yaml, PORTS_FILE)
    print(f"→ Assigned ports: {assigned}. Updated {PORTS_FILE} (backup at {backup_file})")

    # Also write ports to the application’s own vars file
    out_ports = {'ports': {'localhost': {}}}
    for entry, port in assigned.items():
        category, service = entry.split('.', 1)
        out_ports['ports']['localhost'].setdefault(category, {})[service] = port
    ports_file = f'./group_vars/{app_id}_ports.yml'
    dump_yaml(out_ports, ports_file)
    print(f"→ Wrote assigned ports to {ports_file}")


if __name__ == '__main__':
    main()

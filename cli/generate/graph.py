#!/usr/bin/env python3
import os
import argparse
import yaml
import json
from collections import deque
from typing import List, Dict, Any

def find_role_meta(roles_dir: str, role: str) -> str:
    path = os.path.join(roles_dir, role, 'meta', 'main.yml')
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Metadata not found for role: {role}")
    return path

def load_meta(path: str) -> Dict[str, Any]:
    """
    Load meta/main.yml → return galaxy_info + run_after + dependencies
    """
    with open(path, 'r') as f:
        data = yaml.safe_load(f) or {}

    galaxy_info = data.get('galaxy_info', {}) or {}
    return {
        'galaxy_info': galaxy_info,
        'run_after': galaxy_info.get('run_after', []) or [],
        'dependencies': data.get('dependencies', []) or []
    }

def build_single_graph(start_role: str, recurse_on: str, roles_dir: str) -> Dict[str, Any]:
    """
    Build one graph for exactly one dependency type:
      - includes all links for context
      - recurses only on `recurse_on`
    """
    nodes: Dict[str, Dict[str, Any]] = {}
    links: List[Dict[str, str]] = []
    visited = set()
    queue = deque([start_role])

    while queue:
        role = queue.popleft()
        if role in visited:
            continue
        visited.add(role)

        try:
            meta = load_meta(find_role_meta(roles_dir, role))
        except FileNotFoundError:
            continue

        # register node
        node = {'id': role}
        node.update(meta['galaxy_info'])
        node['doc_url']    = f"https://docs.cymais.cloud/roles/{role}/README.html"
        node['source_url'] = f"https://github.com/kevinveenbirkenbach/cymais/tree/master/roles/{role}"
        nodes[role] = node

        # emit all links
        for lt in ('run_after', 'dependencies'):
            for tgt in meta[lt]:
                links.append({'source': role, 'target': tgt, 'type': lt})

        # recurse only on chosen type
        for tgt in meta[recurse_on]:
            if tgt not in visited:
                queue.append(tgt)

    return {'nodes': list(nodes.values()), 'links': links}

def build_graphs(start_role: str, types: List[str], roles_dir: str) -> Dict[str, Any]:
    """
    If multiple types: return { type1: graph1, type2: graph2, ... }
    If single type: return that single graph dict
    """
    if len(types) == 1:
        return build_single_graph(start_role, types[0], roles_dir)
    combined = {}
    for t in types:
        combined[t] = build_single_graph(start_role, t, roles_dir)
    return combined

def output_graph(graph_data: Any, fmt: str, start: str, types: List[str]):
    """
    Write to file or print to console. If multiple types, join them in filename.
    """
    if len(types) == 1:
        base = f"{start}_{types[0]}"
    else:
        base = f"{start}_{'_'.join(types)}"

    if fmt == 'console':
        print(yaml.safe_dump(graph_data, sort_keys=False))
    elif fmt in ('yaml', 'json'):
        path = f"{base}.{fmt}"
        with open(path, 'w') as f:
            if fmt == 'yaml':
                yaml.safe_dump(graph_data, f, sort_keys=False)
            else:
                json.dump(graph_data, f, indent=2)
        print(f"Wrote {fmt.upper()} to {path}")
    else:
        raise ValueError(f"Unknown format: {fmt}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_roles_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'roles'))

    parser = argparse.ArgumentParser(
        description="Generate dependency graphs from Ansible roles' meta/main.yml"
    )
    parser.add_argument(
        '-r', '--role', required=True,
        help="Starting role name (directory under roles/)"
    )
    parser.add_argument(
        '-t', '--type',
        choices=['run_after', 'dependencies'],
        default=['run_after'],
        nargs='+',
        help="Dependency type(s) to recurse on; can specify multiple"
    )
    parser.add_argument(
        '-o', '--output',
        choices=['yaml', 'json', 'console'],
        default='yaml',
        help="Output as files (yaml/json) or print to console"
    )
    parser.add_argument(
        '--roles-dir',
        default=default_roles_dir,
        help=f"Path to the roles directory (default: {default_roles_dir})"
    )
    args = parser.parse_args()

    graph_data = build_graphs(
        start_role=args.role,
        types=args.type,
        roles_dir=args.roles_dir
    )
    output_graph(graph_data, args.output, args.role, args.type)

if __name__ == '__main__':
    main()

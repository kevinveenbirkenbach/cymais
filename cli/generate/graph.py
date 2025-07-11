#!/usr/bin/env python3
import os
import argparse
import yaml
import json
from collections import deque
from typing import List, Dict, Any, Set


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

def build_single_graph(
    start_role: str,
    dep_type: str,
    direction: str,
    roles_dir: str,
    max_depth: int
) -> Dict[str, Any]:
    """
    Build one graph for one dependency type and direction:
      - 'to': follow edges source→target
      - 'from': reverse edges (find roles listing this role)
      - max_depth > 0: limit hops to max_depth
      - max_depth ≤ 0: stop when you’d revisit a node already on the path
    """
    nodes: Dict[str, Dict[str, Any]] = {}
    links: List[Dict[str, str]] = []

    def traverse(role: str, depth: int, path: Set[str]):
        # Register node once
        if role not in nodes:
            meta = load_meta(find_role_meta(roles_dir, role))
            node = {'id': role}
            node.update(meta['galaxy_info'])
            node['doc_url'] = f"https://docs.cymais.cloud/roles/{role}/README.html"
            node['source_url'] = (
                f"https://github.com/kevinveenbirkenbach/cymais/tree/master/roles/{role}"
            )
            nodes[role] = node

        # Depth guard
        if max_depth > 0 and depth >= max_depth:
            return

        # Determine neighbors according to direction
        if direction == 'to':
            neighbors = load_meta(find_role_meta(roles_dir, role)).get(dep_type, [])
            for tgt in neighbors:
                links.append({'source': role, 'target': tgt, 'type': dep_type})
                # General cycle check
                if tgt in path:
                    continue
                traverse(tgt, depth + 1, path | {tgt})

        else:  # direction == 'from'
            # Find all roles that list this role in their dep_type
            for other in os.listdir(roles_dir):
                try:
                    meta_o = load_meta(find_role_meta(roles_dir, other))
                except FileNotFoundError:
                    continue
                if role in meta_o.get(dep_type, []):
                    links.append({'source': other, 'target': role, 'type': dep_type})
                    if other in path:
                        continue
                    traverse(other, depth + 1, path | {other})

    # Kick off recursion
    traverse(start_role, depth=0, path={start_role})
    return {'nodes': list(nodes.values()), 'links': links}

def build_mappings(
    start_role: str,
    mappings: List[Dict[str, str]],
    roles_dir: str,
    max_depth: int
) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for mapping in mappings:
        for dep_type, direction in mapping.items():
            key = f"{dep_type}_{direction}"
            result[key] = build_single_graph(
                start_role, dep_type, direction, roles_dir, max_depth)
    return result


def output_graph(graph_data: Any, fmt: str, start: str, key: str):
    base = f"{start}_{key}"
    if fmt == 'console':
        print(f"--- {base} ---")
        print(yaml.safe_dump(graph_data, sort_keys=False))
    elif fmt in ('yaml', 'json'):
        path = f"{base}.{fmt}"
        with open(path, 'w') as f:
            if fmt == 'yaml':
                yaml.safe_dump(graph_data, f, sort_keys=False)
            else:
                json.dump(graph_data, f, indent=2)
        print(f"Wrote {path}")
    else:
        raise ValueError(f"Unknown format: {fmt}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_roles_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'roles'))

    parser = argparse.ArgumentParser(
        description="Generate graphs based on dependency mappings"
    )
    parser.add_argument(
        '-r', '--role', 
        required=True,
        help="Starting role name"
    )
    parser.add_argument(
        '-m', '--mapping',
        nargs='+',
        default=[
            'run_after:to',
            'run_after:from',
            'dependencies:to',
            'dependencies:from'
        ],
        help="Mapping entries as type:direction (default all 4 combos)"
    )
    parser.add_argument(
        '-D', '--depth',
        type=int,
        default=0,
        help="Max recursion depth (>0) or <=0 to stop on cycle"
    )
    parser.add_argument(
        '-o', '--output',
        choices=['yaml', 'json', 'console'],
        default='console',
        help="Output format"
    )
    parser.add_argument(
        '--roles-dir',
        default=default_roles_dir,
        help="Roles directory"
    )
    args = parser.parse_args()

    mappings: List[Dict[str, str]] = []
    for entry in args.mapping:
        if ':' not in entry:
            parser.error(f"Invalid mapping '{entry}', must be type:direction")
        dep_type, direction = entry.split(':', 1)
        if dep_type not in ('run_after', 'dependencies'):
            parser.error(f"Unknown dependency type '{dep_type}'")
        if direction not in ('to', 'from'):
            parser.error(f"Unknown direction '{direction}'")
        mappings.append({dep_type: direction})

    graphs = build_mappings(
        start_role=args.role,
        mappings=mappings,
        roles_dir=args.roles_dir,
        max_depth=args.depth
    )

    for key, graph_data in graphs.items():
        output_graph(graph_data, args.output, args.role, key)

if __name__ == '__main__':
    main()

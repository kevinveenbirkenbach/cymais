#!/usr/bin/env python3
import os
import argparse
import json
from typing import List, Dict, Any

from cli.generate.graph import build_mappings, output_graph


def find_roles(roles_dir: str):
    """Yield (role_name, role_path) for every subfolder in roles_dir."""
    for entry in os.listdir(roles_dir):
        path = os.path.join(roles_dir, entry)
        if os.path.isdir(path):
            yield entry, path


def main():
    # default roles dir is ../../roles relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_roles_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'roles'))

    parser = argparse.ArgumentParser(
        description="Generate mappings-based graphs for each role and write tree.json"
    )
    parser.add_argument(
        '-d', '--role_dir',
        default=default_roles_dir,
        help=f"Path to roles directory (default: {default_roles_dir})"
    )
    parser.add_argument(
        '-m', '--mapping',
        nargs='+',
        default=[
            'run_after:to', 'run_after:from',
            'dependencies:to', 'dependencies:from'
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
        default='json',
        help="Output format"
    )
    parser.add_argument(
        '-p', '--preview',
        action='store_true',
        help="Preview graphs to console instead of writing files"
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Enable verbose logging"
    )
    args = parser.parse_args()

    # parse mappings
    mappings: List[Dict[str, str]] = []
    for entry in args.mapping:
        if ':' not in entry:
            parser.error(f"Invalid mapping '{entry}', must be type:direction")
        dep_type, direction = entry.split(':', 1)
        mappings.append({dep_type: direction})

    if args.verbose:
        print(f"Roles directory: {args.role_dir}")
        print(f"Mappings: {mappings}")
        print(f"Max depth: {args.depth}")
        print(f"Output format: {args.output}")
        print(f"Preview mode: {args.preview}")

    for role_name, role_path in find_roles(args.role_dir):
        if args.verbose:
            print(f"Processing role: {role_name}")

        # Build graphs for each mapping
        graphs = build_mappings(
            start_role=role_name,
            mappings=mappings,
            roles_dir=args.role_dir,
            max_depth=args.depth
        )

        # Prepare output file or previews
        if args.preview:
            for key, data in graphs.items():
                if args.verbose:
                    print(f"Previewing graph '{key}' for role '{role_name}'")
                output_graph(data, 'console', role_name, key)
        else:
            tree_file = os.path.join(role_path, 'meta', 'tree.json')
            os.makedirs(os.path.dirname(tree_file), exist_ok=True)
            # write combined JSON
            with open(tree_file, 'w') as f:
                json.dump(graphs, f, indent=2)
            if args.verbose:
                print(f"Wrote {tree_file}")
            else:
                print(f"Wrote {tree_file}")

if __name__ == '__main__':
    main()

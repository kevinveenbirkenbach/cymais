#!/usr/bin/env python3
import os
import argparse
import yaml
import json

from cli.generate.graph import build_graphs, output_graph

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
        description="Generate a tree.json for each role, containing both run_after and dependencies"
    )
    parser.add_argument(
        '-d','--role_dir',
        default=default_roles_dir,
        help=f"Path to roles directory (default: {default_roles_dir})"
    )
    parser.add_argument(
        '-p','--preview',
        action='store_true',
        help="Preview all graphs on console instead of writing files"
    )
    args = parser.parse_args()

    for role_name, role_path in find_roles(args.role_dir):
        # Build both graphs at once
        graph_data = build_graphs(
            start_role=role_name,
            types=['run_after','dependencies'],
            roles_dir=args.role_dir
        )

        if args.preview:
            # pretty-print via output_graph as YAML to console
            output_graph(
                graph_data,
                fmt='console',
                start=role_name,
                types=['run_after','dependencies']
            )
        else:
            # write raw JSON into roles/<role>/meta/tree.json
            tree_file = os.path.join(role_path, 'meta', 'tree.json')
            os.makedirs(os.path.dirname(tree_file), exist_ok=True)
            with open(tree_file, 'w') as f:
                json.dump(graph_data, f, indent=2)
            print(f"Wrote {tree_file}")

if __name__ == '__main__':
    main()

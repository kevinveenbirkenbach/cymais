#!/usr/bin/env python3

import os
import re
import subprocess
import sys
import argparse


def extract_domains(config_path):
    """
    Extracts domain names from .conf filenames in the given directory.
    """
    domain_pattern = re.compile(r'^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\.conf$')
    domains = []

    try:
        for filename in os.listdir(config_path):
            if filename.endswith(".conf") and domain_pattern.match(filename):
                domain = filename[:-5]  # Remove ".conf"
                domains.append(domain)
    except FileNotFoundError:
        print(f"Directory {config_path} not found.", file=sys.stderr)
        return None

    return domains


def run_node_checker(script_path, domains):
    """
    Executes the Node.js CSP checker script with the given domains.
    """
    try:
        result = subprocess.run(
            ["node", script_path] + domains,
            check=True
        )
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"{os.path.basename(script_path)} reported issues (exit code {e.returncode})")
        return e.returncode
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(description="Check CSP-blocked resources via Puppeteer")
    parser.add_argument("--nginx-config-dir", required=True, help="Directory containing NGINX .conf files")
    parser.add_argument("--script", required=True, help="Path to Node.js CSP checker script")
    args = parser.parse_args()

    domains = extract_domains(args.nginx_config_dir)

    if domains is None:
        return 1

    if not domains:
        print("No domains found to check.")
        return 0

    return run_node_checker(args.script, domains)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import textwrap

def format_command_help(name, description, indent=2, col_width=36, width=80):
    prefix = " " * indent + f"{name:<{col_width - indent}}"
    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=prefix,
        subsequent_indent=" " * col_width
    )
    return wrapper.fill(description)

def list_cli_commands(cli_dir):
    return sorted(
        os.path.splitext(f.name)[0] for f in os.scandir(cli_dir)
        if f.is_file() and f.name.endswith(".py") and not f.name.startswith("__")
    )

def extract_description_via_help(cli_script_path):
    """Run `script --help` and extract the first non-usage line after usage block."""
    try:
        result = subprocess.run(
            [sys.executable, cli_script_path, "--help"],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.splitlines()

        # Skip until first empty line after usage block
        for i, line in enumerate(lines):
            if line.strip().startswith("usage:"):
                continue
            if line.strip() == "":
                # description usually comes after usage and empty line
                for j in range(i+1, len(lines)):
                    desc = lines[j].strip()
                    if desc:
                        return desc
        return "-"
    except Exception:
        return "-"

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    cli_dir = os.path.join(script_dir, "cli")
    os.chdir(script_dir)

    available_cli_commands = list_cli_commands(cli_dir)

    # Special case: user ran `cymais playbook --help`
    if len(sys.argv) >= 3 and sys.argv[1] in available_cli_commands and sys.argv[2] == "--help":
        cli_script_path = os.path.join(cli_dir, f"{sys.argv[1]}.py")
        subprocess.run([sys.executable, cli_script_path, "--help"])
        sys.exit(0)

    # Global --help
    if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) == 1:
        print("CyMaIS CLI – proxy to tools in ./cli/\n")
        print("Usage:")
        print("  cymais <command> [options]\n")
        print("Available commands:")
        for cmd in available_cli_commands:
            path = os.path.join(cli_dir, f"{cmd}.py")
            desc = extract_description_via_help(path)
            print(format_command_help(cmd, desc))
        print("\nUse 'cymais <command> --help' for details on each command.")
        sys.exit(0)

    # Default flow
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("cli_command", choices=available_cli_commands)
    parser.add_argument("cli_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    cli_script_path = os.path.join(cli_dir, f"{args.cli_command}.py")
    full_cmd = [sys.executable, cli_script_path] + args.cli_args
    subprocess.run(full_cmd, check=True)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

def list_cli_commands(cli_dir):
    return sorted(
        os.path.splitext(f.name)[0] for f in os.scandir(cli_dir)
        if f.is_file() and f.name.endswith(".py") and not f.name.startswith("__")
    )

def extract_docstring(cli_script_path):
    try:
        with open(cli_script_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith(('"""', "'''")):
                    return line.strip().strip('"\'')
                if line.strip().startswith("DESCRIPTION"):
                    return line.split("=", 1)[1].strip().strip("\"'")
    except Exception:
        pass
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
            desc = extract_docstring(path)
            print(f"  {cmd:25} {desc}")
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

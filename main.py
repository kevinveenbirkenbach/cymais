#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
from textwrap import indent

def list_cli_commands(cli_dir):
    """List all available CLI script names in the given directory (without .py extension)."""
    return sorted(
        os.path.splitext(f.name)[0] for f in os.scandir(cli_dir)
        if f.is_file() and f.name.endswith(".py") and not f.name.startswith("__")
    )

def get_help_for_cli_command(cli_script):
    """Return the --help output for a given CLI script path."""
    try:
        result = subprocess.run(
            [sys.executable, cli_script, "--help"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"(⚠️ Help not available: {e})"

def build_full_help(cli_dir, available_cli_commands):
    """Return a composed help string with help snippets from each CLI command."""
    help_output = ["Available CLI commands:\n"]
    for cmd in available_cli_commands:
        cli_path = os.path.join(cli_dir, f"{cmd}.py")
        help_snippet = get_help_for_cli_command(cli_path)
        help_output.append(f"🔹 {cmd}\n{indent(help_snippet, '    ')}\n")
    return "\n".join(help_output)

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    cli_dir = os.path.join(script_dir, "cli")
    os.chdir(script_dir)

    available_cli_commands = list_cli_commands(cli_dir)

    # Custom --help handler
    if "--help" in sys.argv or "-h" in sys.argv:
        parser = argparse.ArgumentParser(
            description="CyMaIS CLI – proxy to tools in ./cli/",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        parser.add_argument("cli_command", choices=available_cli_commands, help="The CLI command to run (proxied from ./cli/)")
        parser.add_argument("cli_args", nargs=argparse.REMAINDER, help="Arguments to pass to the CLI script")
        parser.print_help()
        print()
        print(build_full_help(cli_dir, available_cli_commands))
        sys.exit(0)

    # Standard execution flow
    parser = argparse.ArgumentParser(description="CyMaIS CLI – proxy to tools in ./cli/")
    parser.add_argument("cli_command", choices=available_cli_commands, help="The CLI command to run (proxied from ./cli/)")
    parser.add_argument("cli_args", nargs=argparse.REMAINDER, help="Arguments to pass to the CLI script")
    args = parser.parse_args()

    cli_script_path = os.path.join(cli_dir, f"{args.cli_command}.py")
    full_cmd = [sys.executable, cli_script_path] + args.cli_args
    subprocess.run(full_cmd, check=True)

if __name__ == "__main__":
    main()

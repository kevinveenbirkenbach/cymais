#!/usr/bin/env python3

import argparse
import subprocess
import os
import datetime

def run_ansible_playbook(inventory, playbook, modes, limit=None, password_file=None, verbose=0, skip_tests:bool=False):
    start_time = datetime.datetime.now()
    print(f"\n▶️ Script started at: {start_time.isoformat()}\n")
    
    print("\n🛠️  Building project (make build)...\n")
    subprocess.run(["make", "build"], check=True)

    if not skip_tests:
        print("\n🧪 Running tests (make test)...\n")
        subprocess.run(["make", "test"], check=True)

    cmd = ["ansible-playbook", "-i", inventory, playbook]

    if limit:
        cmd.extend(["--limit", limit])

    for key, value in modes.items():
        val = str(value).lower() if isinstance(value, bool) else str(value)
        cmd.extend(["-e", f"{key}={val}"])

    if password_file:
        cmd.extend(["--vault-password-file", password_file])
    else:
        cmd.extend(["--ask-vault-pass"])

    if verbose:
        cmd.append("-" + "v" * verbose)

    print("\n🚀 Launching Ansible Playbook...\n")
    subprocess.run(cmd, check=True)

    end_time = datetime.datetime.now()
    print(f"\n✅ Script ended at: {end_time.isoformat()}\n")

    duration = end_time - start_time
    print(f"⏱️ Total execution time: {duration}\n")

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser(
        description="Run the central Ansible deployment script to manage infrastructure, updates, and tests."
    )

    parser.add_argument(
        "inventory",
        help="Path to the inventory file (INI or YAML) containing hosts and variables."
    )
    parser.add_argument(
        "--limit",
        help="Restrict execution to a specific host or host group from the inventory."
    )
    parser.add_argument(
        "--host-type",
        choices=["server", "personal-computer"],
        default="server",
        help="Specify whether the target is a server or a personal computer. Affects role selection and variables."
    )
    parser.add_argument(
        "--reset", action="store_true",
        help="Reset all CyMaIS files and configurations, and run the entire playbook (not just individual roles)."
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Run test routines instead of production tasks. Useful for local testing and CI pipelines."
    )
    parser.add_argument(
        "--update", action="store_true",
        help="Enable the update procedure to bring software and roles up to date."
    )
    parser.add_argument(
        "--backup", action="store_true",
        help="Perform a full backup of critical data and configurations before the update process."
    )
    parser.add_argument(
        "--cleanup", action="store_true",
        help="Clean up unused files and outdated configurations after all tasks are complete."
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Enable detailed debug output for Ansible and this script."
    )
    parser.add_argument(
        "--password-file",
        help="Path to the file containing the Vault password. If not provided, prompts for the password interactively."
    )
    parser.add_argument(
        "--skip-tests", action="store_true",
        help="Skip running 'make test' even if tests are normally enabled."
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0,
        help="Increase verbosity level. Multiple -v flags increase detail (e.g., -vvv for maximum log output)."
    )

    args = parser.parse_args()

    modes = {
        "mode_reset": args.reset,
        "mode_test": args.test,
        "mode_update": args.update,
        "mode_backup": args.backup,
        "mode_cleanup": args.cleanup,
        "enable_debug": args.debug,
        "host_type": args.host_type
    }

    playbook_file = os.path.join(os.path.dirname(script_dir), "playbook.yml")

    run_ansible_playbook(
        inventory=args.inventory,
        playbook=playbook_file,
        modes=modes,
        limit=args.limit,
        password_file=args.password_file,
        verbose=args.verbose,
        skip_tests=args.skip_tests
    )

if __name__ == "__main__":
    main()

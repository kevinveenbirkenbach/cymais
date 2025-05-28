#!/usr/bin/env python3

import argparse
import subprocess
import os
import datetime

def run_ansible_playbook(inventory, playbook, modes, limit=None, password_file=None, verbose=0, skip_tests=False):
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
    parser = argparse.ArgumentParser(description="Run Ansible Playbooks")

    parser.add_argument("inventory", help="Path to the inventory file")
    parser.add_argument("--limit", help="Limit execution to a specific server")
    parser.add_argument("--host-type", choices=["server", "personal-computer"], default="server")
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--backup", action="store_true")
    parser.add_argument("--cleanup", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--password-file")
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("-v", "--verbose", action="count", default=0)

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

#!/usr/bin/env python3

import argparse
import subprocess

def run_ansible_vault(action, filename, vault_password_file):
    cmd = ["ansible-vault", action, filename, "--vault-password-file", vault_password_file]
    subprocess.run(cmd, check=True)

def run_ansible_playbook(inventory, playbook, limit=None, extra_vars=None, vault_password_file=None, verbose=False):
    cmd = ["ansible-playbook", "-i", inventory, playbook]
    if limit:
        cmd.extend(["--limit", limit])
    if extra_vars:
        for key, value in extra_vars.items():
            cmd.extend(["-e", f"{key}={str(value).lower()}"])
    if vault_password_file:
        cmd.extend(["--vault-password-file", vault_password_file])
    if verbose:
        cmd.append("-v")
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(description="CyMaIS Ansible Deployment and Vault Management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Vault Subcommands
    vault_parser = subparsers.add_parser("vault", help="Manage Ansible Vault")
    vault_parser.add_argument("action", choices=["edit", "decrypt", "encrypt"], help="Vault action")
    vault_parser.add_argument("filename", help="File to process")
    vault_parser.add_argument("--vault-password-file", required=True, help="Path to the Vault password file")

    # Playbook Subcommands
    playbook_parser = subparsers.add_parser("playbook", help="Run Ansible Playbooks")
    playbook_parser.add_argument("inventory", help="Path to the inventory file")
    playbook_parser.add_argument("playbook", help="Path to the playbook file")
    playbook_parser.add_argument("--limit", help="Limit execution to a specific server")
    playbook_parser.add_argument("--reset", action="store_true", help="Enable reset mode")
    playbook_parser.add_argument("--test", action="store_true", help="Enable test mode")
    playbook_parser.add_argument("--update", action="store_true", help="Enable update mode")
    playbook_parser.add_argument("--backup", action="store_true", help="Enable backup mode")
    playbook_parser.add_argument("--cleanup", action="store_true", help="Enable cleanup mode")
    playbook_parser.add_argument("--debug", action="store_true", help="Enable debugging output")
    playbook_parser.add_argument("--vault-password-file", help="Path to the Vault password file")
    playbook_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    if args.command == "vault":
        run_ansible_vault(args.action, args.filename, args.vault_password_file)
    elif args.command == "playbook":
        extra_vars = {
            "mode_reset": args.reset,
            "mode_test": args.test,
            "mode_update": args.update,
            "mode_backup": args.backup,
            "mode_cleanup": args.cleanup,
            "enable_debug": args.debug,
        }
        extra_vars = {k: v for k, v in extra_vars.items() if v}  # Remove false values
        run_ansible_playbook(args.inventory, args.playbook, args.limit, extra_vars, args.vault_password_file, args.verbose)

if __name__ == "__main__":
    main()

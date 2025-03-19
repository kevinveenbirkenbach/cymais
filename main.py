#!/usr/bin/env python3

import argparse
import subprocess

def run_ansible_vault(action, filename, password_file):
    """Execute an ansible-vault command with the specified action on a file."""
    cmd = ["ansible-vault", action, filename, "--vault-password-file", password_file]
    subprocess.run(cmd, check=True)

def run_ansible_playbook(inventory:str, playbook:str, modes:[bool], limit:str=None, password_file:str=None, verbose:bool=False):
    """Execute an ansible-playbook command with optional parameters."""
    cmd = ["ansible-playbook", "-i", inventory, playbook]
    
    if limit:
        cmd.extend(["--limit", limit])
    
    if modes:
        for key, value in modes.items():
            # Convert boolean values to lowercase strings
            arg_value = f"{str(value).lower()}" if isinstance(value, bool) else f"{value}"
            cmd.extend(["-e", f"{key}={arg_value}"])
    
    if password_file:
        cmd.extend(["--vault-password-file", password_file])
    else:
        cmd.extend(["--ask-vault-pass"])
    
    if verbose:
        cmd.append("-v")
    
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(description="CyMaIS Ansible Deployment and Vault Management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Vault subcommand parser
    vault_parser = subparsers.add_parser("vault", help="Manage Ansible Vault")
    vault_parser.add_argument("action", choices=["edit", "decrypt", "encrypt"], help="Vault action")
    vault_parser.add_argument("filename", help="File to process")
    vault_parser.add_argument("--password-file", required=True, help="Path to the Vault password file")

    # Playbook subcommand parser
    playbook_parser = subparsers.add_parser("playbook", help="Run Ansible Playbooks")
    playbook_parser.add_argument("inventory", help="Path to the inventory file")
    playbook_parser.add_argument("--limit", help="Limit execution to a specific server")
    playbook_parser.add_argument("--host-type", choices=["server", "personal-computer"], default="server",
                                 help="Host type to run the playbook on; defaults to 'server'")
    playbook_parser.add_argument("--reset", action="store_true", help="Enable reset mode")
    playbook_parser.add_argument("--test", action="store_true", help="Enable test mode")
    playbook_parser.add_argument("--update", action="store_true", help="Enable update mode")
    playbook_parser.add_argument("--backup", action="store_true", help="Enable backup mode")
    playbook_parser.add_argument("--cleanup", action="store_true", help="Enable cleanup mode")
    playbook_parser.add_argument("--debug", action="store_true", help="Enable debugging output")
    playbook_parser.add_argument("--password-file", help="Path to the Vault password file")
    playbook_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    if args.command == "vault":
        run_ansible_vault(args.action, args.filename, args.password_file)
    elif args.command == "playbook":
        modes = {
            "mode_reset": args.reset,
            "mode_test": args.test,
            "mode_update": args.update,
            "mode_backup": args.backup,
            "mode_cleanup": args.cleanup,
            "enable_debug": args.debug,
            "host_type": args.host_type
        }

        # Use a fixed playbook file "playbook.yml"
        run_ansible_playbook(args.inventory, "playbook.yml", modes, args.limit, args.password_file, args.verbose)

if __name__ == "__main__":
    main()

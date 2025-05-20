import argparse
import subprocess
import sys
from pathlib import Path
import yaml
from typing import Dict, Any
from utils.manager.inventory import InventoryManager
from utils.handler.vault import VaultHandler, VaultScalar
from utils.handler.yaml import YamlHandler
from yaml.dumper import SafeDumper

def main():
    parser = argparse.ArgumentParser(
        description="Selectively vault credentials + become-password in your inventory."
    )
    parser.add_argument("--role-path", required=True, help="Path to your role")
    parser.add_argument("--inventory-file", required=True, help="Host vars file to update")
    parser.add_argument("--vault-password-file", required=True, help="Vault password file")
    parser.add_argument("--set", nargs="*", default=[], help="Override values key.subkey=VALUE")
    args = parser.parse_args()

    # Parsing overrides
    overrides = {k.strip(): v.strip() for pair in args.set for k, v in [pair.split("=", 1)]}

    # Initialize the Inventory Manager
    manager = InventoryManager(
        role_path=Path(args.role_path),
        inventory_path=Path(args.inventory_file),
        vault_pw=args.vault_password_file,
        overrides=overrides
    )

    # 1) Apply schema and update inventory
    updated_inventory = manager.apply_schema()

    # 2) Vault any leaves under 'credentials:' mappings
    manager.vault_handler.encrypt_leaves(updated_inventory, args.vault_password_file)

    # 3) Vault top-level ansible_become_password if present
    if "ansible_become_password" in updated_inventory:
        val = str(updated_inventory["ansible_become_password"])
        if not val.lstrip().startswith("$ANSIBLE_VAULT"):
            snippet = manager.vault_handler.encrypt_string(val, "ansible_become_password")
            lines = snippet.splitlines()
            indent = len(lines[1]) - len(lines[1].lstrip())
            body = "\n".join(line[indent:] for line in lines[1:])
            updated_inventory["ansible_become_password"] = VaultScalar(body)

    # 4) Save the updated inventory to file
    with open(args.inventory_file, "w", encoding="utf-8") as f:
        yaml.dump(updated_inventory, f, sort_keys=False, Dumper=SafeDumper)

    print(f"✅ Inventory selectively vaulted → {args.inventory_file}")

if __name__ == "__main__":
    main()

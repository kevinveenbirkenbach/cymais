import argparse
import subprocess
import sys
from pathlib import Path
import yaml
from typing import Dict, Any
from utils.manager.inventory import InventoryManager
from utils.handler.vault   import VaultHandler, VaultScalar
from utils.handler.yaml    import YamlHandler
from yaml.dumper import SafeDumper


def ask_for_confirmation(key: str) -> bool:
    """Prompt the user for confirmation to overwrite an existing value."""
    confirmation = input(
        f"Are you sure you want to overwrite the value for '{key}'? (y/n): "
    ).strip().lower()
    return confirmation == 'y'


def main():
    parser = argparse.ArgumentParser(
        description="Selectively vault credentials + become-password in your inventory."
    )
    parser.add_argument(
        "--role-path", required=True, help="Path to your role"
    )
    parser.add_argument(
        "--inventory-file", required=True, help="Host vars file to update"
    )
    parser.add_argument(
        "--vault-password-file", required=True, help="Vault password file"
    )
    parser.add_argument(
        "--set", nargs="*", default=[], help="Override values key.subkey=VALUE"
    )
    parser.add_argument(
        "-f", "--force", action="store_true",
        help="Force overwrite without confirmation"
    )
    args = parser.parse_args()

    # Parse overrides
    overrides = {
        k.strip(): v.strip()
        for pair in args.set for k, v in [pair.split("=", 1)]
    }

    # Initialize inventory manager
    manager = InventoryManager(
        role_path=Path(args.role_path),
        inventory_path=Path(args.inventory_file),
        vault_pw=args.vault_password_file,
        overrides=overrides
    )

    # Load existing credentials to preserve
    existing_apps = manager.inventory.get("applications", {})
    existing_creds = {}
    if manager.app_id in existing_apps:
        existing_creds = existing_apps[manager.app_id].get("credentials", {}).copy()

    # Apply schema (may generate defaults)
    updated_inventory = manager.apply_schema()

    # Restore existing database_password if present
    apps = updated_inventory.setdefault("applications", {})
    app_block = apps.setdefault(manager.app_id, {})
    creds = app_block.setdefault("credentials", {})
    if "database_password" in existing_creds:
        creds["database_password"] = existing_creds["database_password"]

    # Store original plaintext values
    original_plain = {key: str(val) for key, val in creds.items()}

    for key, raw_val in list(creds.items()):
        # Skip if already vaulted
        if isinstance(raw_val, VaultScalar) or str(raw_val).lstrip().startswith("$ANSIBLE_VAULT"):
            continue

        # Determine plaintext
        plain = original_plain.get(key, "")
        if key in overrides and (args.force or ask_for_confirmation(key)):
            plain = overrides[key]

        # Encrypt the plaintext
        encrypted = manager.vault_handler.encrypt_string(plain, key)
        lines = encrypted.splitlines()
        indent = len(lines[1]) - len(lines[1].lstrip())
        body = "\n".join(line[indent:] for line in lines[1:])
        creds[key] = VaultScalar(body)

    # Vault top-level become password if present
    if "ansible_become_password" in updated_inventory:
        val = str(updated_inventory["ansible_become_password"])
        if val.lstrip().startswith("$ANSIBLE_VAULT"):
            updated_inventory["ansible_become_password"] = VaultScalar(val)
        else:
            snippet = manager.vault_handler.encrypt_string(
                val, "ansible_become_password"
            )
            lines = snippet.splitlines()
            indent = len(lines[1]) - len(lines[1].lstrip())
            body = "\n".join(line[indent:] for line in lines[1:])
            updated_inventory["ansible_become_password"] = VaultScalar(body)

    # Write back to file
    with open(args.inventory_file, "w", encoding="utf-8") as f:
        yaml.dump(updated_inventory, f, sort_keys=False, Dumper=SafeDumper)

    print(f"✅ Inventory selectively vaulted → {args.inventory_file}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import secrets
import hashlib
import bcrypt
import subprocess
from pathlib import Path

import yaml
from yaml.loader import SafeLoader
from yaml.dumper import SafeDumper

# ─────────────────────────────────────────────────────────────────────────────
# On load: treat any !vault tag as plain text
def _vault_constructor(loader, node):
    return node.value
SafeLoader.add_constructor('!vault', _vault_constructor)

# A str subclass so PyYAML emits !vault literal blocks on dump
class VaultScalar(str):
    pass

def _vault_representer(dumper, data):
    return dumper.represent_scalar('!vault', data, style='|')

SafeDumper.add_representer(VaultScalar, _vault_representer)
# ─────────────────────────────────────────────────────────────────────────────

def generate_value(algorithm: str) -> str:
    if algorithm == "random_hex":
        return secrets.token_hex(64)
    if algorithm == "sha256":
        return hashlib.sha256(secrets.token_bytes(32)).hexdigest()
    if algorithm == "sha1":
        return hashlib.sha1(secrets.token_bytes(20)).hexdigest()
    if algorithm == "bcrypt":
        pw = secrets.token_urlsafe(16).encode()
        return bcrypt.hashpw(pw, bcrypt.gensalt()).decode()
    if algorithm == "plain":
        return secrets.token_urlsafe(32)
    return "undefined"

def wrap_existing_vaults(node):
    """
    Recursively walk the data and wrap any str that begins with
    '$ANSIBLE_VAULT' in a VaultScalar so it dumps as a literal.
    """
    if isinstance(node, dict):
        return {k: wrap_existing_vaults(v) for k, v in node.items()}
    if isinstance(node, list):
        return [wrap_existing_vaults(v) for v in node]
    if isinstance(node, str) and node.lstrip().startswith("$ANSIBLE_VAULT"):
        return VaultScalar(node)
    return node

def load_yaml_plain(path: Path) -> dict:
    """
    Load any YAML (vaulted or not) via SafeLoader + our !vault constructor,
    then wrap existing vault‐blocks for correct literal dumping.
    """
    text = path.read_text()
    data = yaml.load(text, Loader=SafeLoader) or {}
    return wrap_existing_vaults(data)

def encrypt_with_vault(value: str, name: str, vault_password_file: str) -> str:
    cmd = [
        "ansible-vault", "encrypt_string",
        value, f"--name={name}",
        "--vault-password-file", vault_password_file
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ansible-vault encrypt_string failed:\n{proc.stderr}")
    return proc.stdout

def parse_overrides(pairs: list[str]) -> dict:
    out = {}
    for p in pairs:
        if "=" in p:
            k, v = p.split("=", 1)
            out[k.strip()] = v.strip()
    return out

def load_application_id(role_path: Path) -> str:
    vars_file = role_path / "vars" / "main.yml"
    data = load_yaml_plain(vars_file)
    app_id = data.get("application_id")
    if not app_id:
        raise KeyError(f"'application_id' missing in {vars_file}")
    return app_id

def apply_schema(schema: dict,
                 inventory: dict,
                 app_id: str,
                 overrides: dict,
                 vault_pw: str) -> dict:
    apps = inventory.setdefault("applications", {})
    target = apps.setdefault(app_id, {})

    def recurse(branch: dict, dest: dict, prefix: str = ""):
        for key, meta in branch.items():
            full = f"{prefix}.{key}" if prefix else key

            # leaf node
            if isinstance(meta, dict) and all(k in meta for k in ("description","algorithm","validation")):
                plain = overrides.get(full, generate_value(meta["algorithm"]))
                snippet = encrypt_with_vault(plain, key, vault_pw)
                lines = snippet.splitlines()
                indent = len(lines[1]) - len(lines[1].lstrip())
                body = "\n".join(line[indent:] for line in lines[1:])
                dest[key] = VaultScalar(body)

            # nested mapping
            elif isinstance(meta, dict):
                sub = dest.setdefault(key, {})
                recurse(meta, sub, full)

            # literal passthrough
            else:
                dest[key] = meta

    recurse(schema, target)
    return inventory

def encrypt_leaves(branch: dict, vault_pw: str):
    for k, v in list(branch.items()):
        if isinstance(v, dict):
            encrypt_leaves(v, vault_pw)
        else:
            plain = str(v)
            if plain.lstrip().startswith("$ANSIBLE_VAULT"):
                continue
            snippet = encrypt_with_vault(plain, k, vault_pw)
            lines = snippet.splitlines()
            indent = len(lines[1]) - len(lines[1].lstrip())
            body = "\n".join(line[indent:] for line in lines[1:])
            branch[k] = VaultScalar(body)

def encrypt_credentials_branch(node, vault_pw: str):
    if isinstance(node, dict):
        for key, val in node.items():
            if key == "credentials" and isinstance(val, dict):
                encrypt_leaves(val, vault_pw)
            else:
                encrypt_credentials_branch(val, vault_pw)
    elif isinstance(node, list):
        for item in node:
            encrypt_credentials_branch(item, vault_pw)

def main():
    parser = argparse.ArgumentParser(
        description="Selectively vault credentials + become-password in your inventory."
    )
    parser.add_argument("--role-path",         required=True, help="Path to your role")
    parser.add_argument("--inventory-file",    required=True, help="host_vars file to update")
    parser.add_argument("--vault-password-file", required=True, help="Vault password file")
    parser.add_argument("--set", nargs="*", default=[], help="Override values key.subkey=VALUE")
    args = parser.parse_args()

    role_path = Path(args.role_path)
    inv_file   = Path(args.inventory_file)
    vault_pw   = args.vault_password_file
    overrides  = parse_overrides(args.set)

    # 1) Load & wrap existing vault blocks
    inventory = load_yaml_plain(inv_file)

    # 2) Merge in any schema-driven credentials
    schema = load_yaml_plain(role_path / "meta" / "schema.yml")
    app_id = load_application_id(role_path)
    inventory = apply_schema(schema, inventory, app_id, overrides, vault_pw)

    # 3) Vault any leaves under 'credentials:' mappings
    encrypt_credentials_branch(inventory, vault_pw)

    # 4) Vault top-level ansible_become_password if present
    if "ansible_become_password" in inventory:
        val = str(inventory["ansible_become_password"])
        if not val.lstrip().startswith("$ANSIBLE_VAULT"):
            snippet = encrypt_with_vault(val, "ansible_become_password", vault_pw)
            lines = snippet.splitlines()
            indent = len(lines[1]) - len(lines[1].lstrip())
            body = "\n".join(line[indent:] for line in lines[1:])
            inventory["ansible_become_password"] = VaultScalar(body)

    # 5) Overwrite file with proper !vault | blocks only where needed
    with open(inv_file, "w") as f:
        yaml.dump(inventory, f, sort_keys=False, Dumper=SafeDumper)

    print(f"✅ Inventory selectively vaulted → {inv_file}")

if __name__ == "__main__":
    main()

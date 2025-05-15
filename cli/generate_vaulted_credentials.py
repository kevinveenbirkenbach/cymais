#!/usr/bin/env python3
import argparse
import secrets
import hashlib
import bcrypt
import subprocess
from pathlib import Path

import yaml
from yaml.loader import SafeLoader

# ─────────────────────────────────────────────────────────────────────────────
# Let PyYAML treat !vault blocks as ordinary multiline strings
def _vault_constructor(loader, node):
    return node.value
SafeLoader.add_constructor('!vault', _vault_constructor)

# VaultScalar so PyYAML emits a !vault literal block on output
class VaultScalar(str):
    pass

def _vault_representer(dumper, data):
    return dumper.represent_scalar('!vault', data, style='|')

yaml.SafeDumper.add_representer(VaultScalar, _vault_representer)
# ─────────────────────────────────────────────────────────────────────────────

def generate_value(algorithm):
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

def decrypt_inventory(path: Path, vault_password_file: str):
    """
    Try `ansible-vault view`; on "not vaulted" fallback to yaml.safe_load
    (with !vault constructor).
    """
    proc = subprocess.run(
        ["ansible-vault", "view", str(path), "--vault-password-file", vault_password_file],
        capture_output=True, text=True
    )
    if proc.returncode == 0:
        return yaml.safe_load(proc.stdout) or {}
    # fallback if not vaulted
    if "not a vault encrypted file" in proc.stderr.lower():
        return yaml.safe_load(path.read_text()) or {}
    raise RuntimeError(f"ansible-vault view failed:\n{proc.stderr}")

def encrypt_with_vault(value: str, name: str, vault_password_file: str):
    cmd = [
        "ansible-vault", "encrypt_string",
        value, f"--name={name}",
        "--vault-password-file", vault_password_file
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ansible-vault encrypt_string failed:\n{proc.stderr}")
    return proc.stdout

def load_yaml(path: Path):
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}

def save_yaml(path: Path, data):
    path.write_text(yaml.dump(data, sort_keys=False, Dumper=yaml.SafeDumper))

def parse_overrides(pairs):
    out = {}
    for p in pairs:
        if "=" in p:
            k, v = p.split("=", 1)
            out[k.strip()] = v.strip()
    return out

def load_application_id(role_path: Path):
    vars_file = role_path / "vars" / "main.yml"
    if not vars_file.exists():
        raise FileNotFoundError(f"{vars_file} not found")
    data = load_yaml(vars_file)
    app_id = data.get("application_id")
    if not app_id:
        raise KeyError(f"'application_id' missing in {vars_file}")
    return app_id

def apply_schema(schema: dict,
                 inventory: dict,
                 app_id: str,
                 overrides: dict,
                 vault_pw: str):
    apps = inventory.setdefault("applications", {})
    target = apps.setdefault(app_id, {})

    def recurse(branch, dest, prefix=""):
        for key, meta in branch.items():
            full = f"{prefix}.{key}" if prefix else key

            # leaf spec
            if isinstance(meta, dict) and all(k in meta for k in ("description","algorithm","validation")):
                plain = overrides.get(full, generate_value(meta["algorithm"]))
                snippet = encrypt_with_vault(plain, key, vault_pw)
                lines = snippet.splitlines()
                indent = len(lines[1]) - len(lines[1].lstrip())
                body = "\n".join(line[indent:] for line in lines[1:])
                dest[key] = VaultScalar(body)

            # nested
            elif isinstance(meta, dict):
                sub = dest.setdefault(key, {})
                recurse(meta, sub, full)

            # passthrough
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
        for k, v in node.items():
            if k == "credentials" and isinstance(v, dict):
                encrypt_leaves(v, vault_pw)
            else:
                encrypt_credentials_branch(v, vault_pw)
    elif isinstance(node, list):
        for item in node:
            encrypt_credentials_branch(item, vault_pw)

def main():
    parser = argparse.ArgumentParser(
        description="Selectively vault credentials + become-password in an inventory file"
    )
    parser.add_argument("--role-path",  required=True,
                        help="Path to your Ansible role")
    parser.add_argument("--inventory-file", required=True,
                        help="Vaulted host_vars file to update")
    parser.add_argument("--vault-password-file", required=True,
                        help="Ansible Vault password file")
    parser.add_argument("--set", nargs="*", default=[],
                        help="Override values as key.subkey=VALUE")
    args = parser.parse_args()

    role_path = Path(args.role_path)
    inv_file   = Path(args.inventory_file)
    vault_pw   = args.vault_password_file
    overrides  = parse_overrides(args.set)

    app_id = load_application_id(role_path)

    # 1) decrypt-or-plain-load
    inventory = decrypt_inventory(inv_file, vault_pw)

    # 2) merge schema-driven credentials
    schema = load_yaml(role_path / "meta" / "schema.yml")
    inventory = apply_schema(schema, inventory, app_id, overrides, vault_pw)

    # 3) vault leaves under credentials:
    encrypt_credentials_branch(inventory, vault_pw)

    # 4) vault top-level become password
    if "ansible_become_password" in inventory:
        val = str(inventory["ansible_become_password"])
        if not val.lstrip().startswith("$ANSIBLE_VAULT"):
            snippet = encrypt_with_vault(val, "ansible_become_password", vault_pw)
            lines = snippet.splitlines()
            indent = len(lines[1]) - len(lines[1].lstrip())
            body = "\n".join(line[indent:] for line in lines[1:])
            inventory["ansible_become_password"] = VaultScalar(body)

    # 5) write back YAML
    save_yaml(inv_file, inventory)
    print(f"✅ Inventory selectively vaulted → {inv_file}")

if __name__ == "__main__":
    main()

import yaml
import argparse
import secrets
import hashlib
import bcrypt
import subprocess
from pathlib import Path

def prompt(text, default=None):
    """Prompt the user for input, with optional default value."""
    prompt_text = f"[?] {text}" + (f" [{default}]" if default else "") + ": "
    response = input(prompt_text)
    return response.strip() or default

def generate_value(algorithm):
    """Generate a value based on the provided algorithm."""
    if algorithm == "random_hex":
        return secrets.token_hex(64)
    elif algorithm == "sha256":
        return hashlib.sha256(secrets.token_bytes(32)).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(secrets.token_bytes(20)).hexdigest()
    elif algorithm == "bcrypt":
        password = secrets.token_urlsafe(16).encode()
        return bcrypt.hashpw(password, bcrypt.gensalt()).decode()
    elif algorithm == "plain":
        return secrets.token_urlsafe(32)
    else:
        return "undefined"

def encrypt_with_vault(value, name, vault_password_file=None, ask_vault_pass=False):
    """Encrypt the given string using Ansible Vault."""
    cmd = ["ansible-vault", "encrypt_string", value, f"--name={name}"]
    if vault_password_file:
        cmd += ["--vault-password-file", vault_password_file]
    elif ask_vault_pass:
        cmd += ["--ask-vault-pass"]
    else:
        raise RuntimeError("You must provide --vault-password-file or use --ask-vault-pass.")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Vault encryption failed:\n{result.stderr}")
    return result.stdout.strip()

def load_yaml_file(path):
    """Load a YAML file or return an empty dict if not found."""
    if path.exists():
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}
    return {}

def save_yaml_file(path, data):
    """Save a dictionary to a YAML file."""
    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=False)

def parse_overrides(pairs):
    """Parse key=value overrides into a dictionary."""
    result = {}
    for pair in pairs:
        if "=" not in pair:
            continue
        k, v = pair.split("=", 1)
        result[k.strip()] = v.strip()
    return result

def apply_schema_to_inventory(schema, inventory_data, app_id, overrides, vault_password_file, ask_vault_pass):
    """Merge schema into inventory under applications.{app_id}, encrypting all values."""
    inventory_data.setdefault("applications", {})
    applications = inventory_data["applications"]

    if "applications" not in schema or app_id not in schema["applications"]:
        raise KeyError(f"Schema must contain 'applications.{app_id}'")

    app_schema = schema["applications"][app_id]
    applications.setdefault(app_id, {})

    def process_branch(branch, target, path_prefix=""):
        for key, meta in branch.items():
            full_key_path = f"{path_prefix}.{key}" if path_prefix else key
            if isinstance(meta, dict) and all(k in meta for k in ["description", "algorithm", "validation"]):
                if key in target:
                    overwrite = prompt(f"Key '{full_key_path}' already exists. Overwrite?", "n").lower() == "y"
                    if not overwrite:
                        continue
                plain_value = overrides.get(full_key_path, generate_value(meta["algorithm"]))
                vaulted_value = encrypt_with_vault(plain_value, key, vault_password_file, ask_vault_pass)
                target[key] = yaml.load(vaulted_value, Loader=yaml.SafeLoader)
            elif isinstance(meta, dict):
                target.setdefault(key, {})
                process_branch(meta, target[key], full_key_path)
            else:
                target[key] = meta

    process_branch(app_schema, applications[app_id])
    return inventory_data

def main():
    parser = argparse.ArgumentParser(description="Generate Vault-encrypted credentials from schema and write to inventory.")
    parser.add_argument("--role-path", help="Path to the Ansible role")
    parser.add_argument("--inventory-file", help="Path to the inventory file to update")
    parser.add_argument("--application-id", help="Application ID to process (e.g. bigbluebutton)")
    parser.add_argument("--vault-password-file", help="Path to Ansible Vault password file")
    parser.add_argument("--ask-vault-pass", action="store_true", help="Prompt for vault password")
    parser.add_argument("--set", nargs="*", default=[], help="Override values as key=value")
    args = parser.parse_args()

    # Prompt for missing values
    role_path = Path(args.role_path or prompt("Path to Ansible role", "./roles/docker-bigbluebutton"))
    inventory_file = Path(args.inventory_file or prompt("Path to inventory file", "./host_vars/localhost.yml"))
    app_id = args.application_id or prompt("Application ID", "bigbluebutton")

    if not args.vault_password_file and not args.ask_vault_pass:
        print("[?] No Vault password method provided.")
        print("    1) Provide path to --vault-password-file")
        print("    2) Use interactive prompt (--ask-vault-pass)")
        choice = prompt("Select method", "1")
        if choice == "1":
            args.vault_password_file = prompt("Vault password file", "~/.vault_pass.txt").replace("~", str(Path.home()))
        else:
            args.ask_vault_pass = True

    # Load files
    schema_path = role_path / "meta" / "schema.yml"
    schema_data = load_yaml_file(schema_path)
    inventory_data = load_yaml_file(inventory_file)
    overrides = parse_overrides(args.set)

    # Process and save
    updated = apply_schema_to_inventory(
        schema=schema_data,
        inventory_data=inventory_data,
        app_id=app_id,
        overrides=overrides,
        vault_password_file=args.vault_password_file,
        ask_vault_pass=args.ask_vault_pass
    )

    save_yaml_file(inventory_file, updated)
    print(f"\n✅ Inventory file updated at: {inventory_file}")

if __name__ == "__main__":
    main()

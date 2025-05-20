import secrets
import hashlib
import bcrypt
from pathlib import Path
from typing import Dict
from utils.handler.yaml import YamlHandler
from utils.handler.vault import VaultHandler, VaultScalar
import string

class InventoryManager:
    def __init__(self, role_path: Path, inventory_path: Path, vault_pw: str, overrides: Dict[str, str]):
        """Initialize the Inventory Manager."""
        self.role_path = role_path
        self.inventory_path = inventory_path
        self.vault_pw = vault_pw
        self.overrides = overrides
        self.inventory = YamlHandler.load_yaml(inventory_path)
        self.schema = YamlHandler.load_yaml(role_path / "meta" / "schema.yml")
        self.app_id = self.load_application_id(role_path)

        self.vault_handler = VaultHandler(vault_pw)

    def load_application_id(self, role_path: Path) -> str:
        """Load the application ID from the role's vars/main.yml file."""
        vars_file = role_path / "vars" / "main.yml"
        data = YamlHandler.load_yaml(vars_file)
        app_id = data.get("application_id")
        if not app_id:
            print(f"ERROR: 'application_id' missing in {vars_file}", file=sys.stderr)
            sys.exit(1)
        return app_id

    def apply_schema(self) -> Dict:
        """Apply the schema and return the updated inventory."""
        apps = self.inventory.setdefault("applications", {})
        target = apps.setdefault(self.app_id, {})

        # Load the data from vars/main.yml
        vars_file = self.role_path / "vars" / "configuration.yml"
        data = YamlHandler.load_yaml(vars_file)

        # Check if 'central-database' is enabled in the features section of data
        if "features" in data and \
        "central_database" in data["features"] and \
        data["features"]["central_database"]:
            # Add 'central_database' value (password) to credentials
            target.setdefault("credentials", {})["database_password"] = self.generate_value("alphanumeric")

        # Apply recursion only for the `credentials` section
        self.recurse_credentials(self.schema, target)
        return self.inventory

    def recurse_credentials(self, branch: dict, dest: dict, prefix: str = ""):
        """Recursively process only the 'credentials' section and generate values."""
        for key, meta in branch.items():
            full_key = f"{prefix}.{key}" if prefix else key
        
            # Only process 'credentials' section for encryption
            if prefix == "credentials" and isinstance(meta, dict) and all(k in meta for k in ("description", "algorithm", "validation")):
                alg = meta["algorithm"]
                if alg == "plain":
                    # Must be supplied via --set
                    if full_key not in self.overrides:
                        print(f"ERROR: Plain algorithm for '{full_key}' requires override via --set {full_key}=<value>", file=sys.stderr)
                        sys.exit(1)
                    plain = self.overrides[full_key]
                else:
                    plain = self.overrides.get(full_key, self.generate_value(alg))
        
                # Check if the value is already vaulted or if it's a dictionary
                existing_value = dest.get(key)
                
                # If existing_value is a dictionary, print a warning and skip encryption
                if isinstance(existing_value, dict):
                    print(f"Skipping encryption for '{key}', as it is a dictionary.")
                    continue
                
                # Check if the value is a VaultScalar and already vaulted
                if existing_value and isinstance(existing_value, VaultScalar):
                    print(f"Skipping encryption for '{key}', as it is already vaulted.")
                    continue
                
                # Encrypt only if it's not already vaulted
                snippet = self.vault_handler.encrypt_string(plain, key)
                lines = snippet.splitlines()
                indent = len(lines[1]) - len(lines[1].lstrip())
                body = "\n".join(line[indent:] for line in lines[1:])
                dest[key] = VaultScalar(body)
        
            elif isinstance(meta, dict):
                sub = dest.setdefault(key, {})
                self.recurse_credentials(meta, sub, full_key)
            else:
                dest[key] = meta


    def generate_secure_alphanumeric(self, length: int) -> str:
        """Generate a cryptographically secure random alphanumeric string of the given length."""
        characters = string.ascii_letters + string.digits  # a-zA-Z0-9
        return ''.join(secrets.choice(characters) for _ in range(length))

    def generate_value(self, algorithm: str) -> str:
        """Generate a value based on the provided algorithm."""
        if algorithm == "random_hex":
            return secrets.token_hex(64)
        if algorithm == "sha256":
            return hashlib.sha256(secrets.token_bytes(32)).hexdigest()
        if algorithm == "sha1":
            return hashlib.sha1(secrets.token_bytes(20)).hexdigest()
        if algorithm == "bcrypt":
            pw = secrets.token_urlsafe(16).encode()
            return bcrypt.hashpw(pw, bcrypt.gensalt()).decode()
        if algorithm == "alphanumeric":
            return self.generate_secure_alphanumeric(64)
        return "undefined"

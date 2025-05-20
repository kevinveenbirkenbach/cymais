import argparse
import subprocess
from ansible.parsing.vault import VaultLib, VaultSecret
import sys
import yaml
import re
from utils.handler.vault import VaultScalar
from yaml.loader import SafeLoader
from yaml.dumper import SafeDumper

# Register the custom constructor and representer for VaultScalar in PyYAML
SafeLoader.add_constructor('!vault', lambda loader, node: VaultScalar(node.value))
SafeDumper.add_representer(VaultScalar, lambda dumper, data: dumper.represent_scalar('!vault', data))

def is_vault_encrypted_data(data: str) -> bool:
    """Check if the given data is encrypted with Ansible Vault by looking for the vault header."""
    return data.lstrip().startswith('$ANSIBLE_VAULT')

def decrypt_vault_data(encrypted_data: str, vault_secret: VaultSecret) -> str:
    """
    Decrypt the given encrypted data using the provided vault_secret.
    :param encrypted_data: Encrypted string to be decrypted
    :param vault_secret: The VaultSecret instance used to decrypt the data
    :return: Decrypted data as a string
    """
    vault = VaultLib()
    decrypted_data = vault.decrypt(encrypted_data, vault_secret)
    return decrypted_data

def decrypt_vault_file(vault_file: str, vault_password_file: str):
    """
    Decrypt the Ansible Vault file and return its contents.
    :param vault_file: Path to the encrypted Ansible Vault file
    :param vault_password_file: Path to the file containing the Vault password
    :return: Decrypted contents of the Vault file
    """
    # Read the vault password
    with open(vault_password_file, 'r') as f:
        vault_password = f.read().strip()

    # Create a VaultSecret instance from the password
    vault_secret = VaultSecret(vault_password.encode())

    # Read the encrypted file
    with open(vault_file, 'r') as f:
        file_content = f.read()

    # If the file is partially encrypted, we'll decrypt only the encrypted values
    decrypted_data = file_content  # Start with the unmodified content

    # Find all vault-encrypted values (i.e., values starting with $ANSIBLE_VAULT)
    encrypted_values = re.findall(r'^\s*([\w\.\-_]+):\s*["\']?\$ANSIBLE_VAULT[^\n]+', file_content, flags=re.MULTILINE)

    # If there are encrypted values, decrypt them
    for value in encrypted_values:
        # Extract the encrypted value and decrypt it
        encrypted_value = re.search(r'(["\']?\$ANSIBLE_VAULT[^\n]+)', value)
        if encrypted_value:
            # Remove any newlines or extra spaces from the encrypted value
            encrypted_value = encrypted_value.group(0).replace('\n', '').replace('\r', '')
            decrypted_value = decrypt_vault_data(encrypted_value, vault_secret)
            # Replace the encrypted value with the decrypted value in the content
            decrypted_data = decrypted_data.replace(encrypted_value, decrypted_value.strip())

    return decrypted_data

def decrypt_and_display(vault_file: str, vault_password_file: str):
    """
    Decrypts the Ansible Vault file and its values, then display the result.
    Supports both full file and partial value encryption.
    :param vault_file: Path to the encrypted Ansible Vault file
    :param vault_password_file: Path to the file containing the Vault password
    """
    decrypted_data = decrypt_vault_file(vault_file, vault_password_file)

    # Convert the decrypted data to a string format (YAML or JSON)
    output_data = yaml.dump(yaml.safe_load(decrypted_data), default_flow_style=False)

    # Use subprocess to call `less` for paginated, scrollable output
    subprocess.run(["less"], input=output_data, text=True)

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Decrypt and display variables from an Ansible Vault file.")
    
    # Add arguments for the vault file and vault password file
    parser.add_argument(
        'vault_file', 
        type=str, 
        help="Path to the encrypted Ansible Vault file"
    )
    parser.add_argument(
        'vault_password_file', 
        type=str, 
        help="Path to the file containing the Vault password"
    )
    
    # Parse the arguments
    args = parser.parse_args()

    # Display vault variables in a scrollable manner
    decrypt_and_display(args.vault_file, args.vault_password_file)

if __name__ == "__main__":
    main()

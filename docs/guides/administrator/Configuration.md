# Configuration

## Ansible Vault Basics

Infinito.Nexus uses Ansible Vault to protect sensitive data (e.g. passwords). Use these common commands:

### Edit an Encrypted File
```bash
ansible-vault edit <filename.yml> --vault-password-file <your-vault-pass-file>
```

### Decrypt a File
```bash
ansible-vault decrypt <filename.yml> --vault-password-file <your-vault-pass-file>
```

### Encrypt a File
```bash
ansible-vault encrypt <filename.yml> --vault-password-file <your-vault-pass-file>
```

### Encrypt a String
```bash
ansible-vault encrypt_string --vault-password-file <your-vault-pass-file> 'example' --name 'test'
```

## Password Generation

You can generate a secure random password and encrypt it with Ansible Vault. For example:
```bash
ansible-vault encrypt_string "$(cat /dev/urandom | tr -dc 'A-Za-z0-9' | head -c 32)" --vault-password-file /path/to/your/vault_pass.txt | xclip -selection clipboard
```
This command generates a 32-character alphanumeric password, encrypts it, and copies the result to your clipboard.

## Final Notes

- **Customizing Paths and Variables:**  
  All file paths and configuration variables are defined in group variables (e.g., `group_vars/all/*.yml`) and role variable files. Adjust these to suit your deployment environment.
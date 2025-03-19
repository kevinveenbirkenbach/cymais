# Deploy

This guide explains how to deploy and manage the Cyber Master Infrastructure Solution (CyMaIS) using Ansible. CyMaIS is based on a collection of ansible tasks. The tasks use different “modes” to control behavior such as updates, backups, resets, and cleanup tasks. 

## Prerequisites
- **Inventory File:** Have an inventory file that lists your servers and PCs. (Paths in examples are general; adjust them to your environment.)
- **Cymais Installed:** CyMaIS is installed via [Kevin's Package-Manager](https://github.com/kevinveenbirkenbach/package-manager).
- **Vault Password File (Optional):** Prepare a file with your vault password if you prefer not to enter it interactively.

## Deploying on Servers
To get detailled information how to use CyMaIS to deploy software to your server execute:
```sh
cymais --help
```

## Using a Password File

To avoid entering your vault password interactively every time, use the `--password-file` option:
```bash
--password-file /path/to/your/vault_pass.txt
```
Ensure the vault password file is stored securely.

# Installation

This guide explains how to deploy and manage the Cyber Master Infrastructure Solution (CyMaIS) using Ansible. CyMaIS is based on a collection of playbooks that are designed for your servers and personal computers. The playbooks use different “modes” to control behavior such as updates, backups, resets, and cleanup tasks. This document outlines how to use Ansible Vault, describes the various operating modes, and shows example commands to run the playbooks.


This guide should give you a comprehensive starting point for managing your infrastructure with CyMaIS. For further details, consult the individual role documentation and the accompanying repository README files.

## Prerequisites
- **Inventory File:** Have an inventory file that lists your servers and PCs. (Paths in examples are general; adjust them to your environment.)
- **Vault Password File (Optional):** Prepare a file with your vault password if you prefer not to enter it interactively.

## Operating Modes

CyMaIS playbooks support several modes that control which tasks are executed:

- **mode_reset** (`true`/`false`):  
  When enabled, cleans up all CyMaIS-related files. Use this mode when you need to reinitialize the system completely. _Note: Run the full playbook when using reset mode._

- **mode_test** (`true`/`false`):  
  Executes test routines instead of production routines. Useful for staging or validation.

- **mode_update** (`true`/`false`):  
  Enables update tasks to upgrade packages and Docker images. Set to `false` if you want to skip updates.

- **mode_backup** (`true`/`false`):  
  Activates backup procedures before applying updates. This ensures your data is backed up prior to any changes.

- **mode_cleanup** (`true`/`false`):  
  Performs cleanup of unused files and configurations (e.g., removing obsolete certificates or Docker volumes).

These modes are defined in your group variables (e.g., in a file like `group_vars/all/01_modes.yml`) and can be overridden via extra variables when running playbooks.

---

## Deploying on Servers

To deploy CyMaIS on your servers, use an Ansible playbook that targets your server inventory. Below are some example commands:

### Configure All Servers
```bash
ansible-playbook -i /path/to/your/inventory/servers.yml "$(pkgmgr path cymais)playbook.servers.yml" --ask-vault-pass
```

### Configure a Specific Server
For example, to target a server named `galaxyserver`:
```bash
ansible-playbook -i /path/to/your/inventory/servers.tmp "$(pkgmgr path cymais)playbook.servers.yml" --limit galaxyserver --ask-vault-pass
```

### Run in Temporary Mode Without Update
```bash
ansible-playbook -i /path/to/your/inventory/servers.tmp "$(pkgmgr path cymais)playbook.servers.yml" --limit galaxyserver -e "mode_update=false" --ask-vault-pass
```

### Run Without Update and Backup
```bash
ansible-playbook -i /path/to/your/inventory/servers.tmp "$(pkgmgr path cymais)playbook.servers.yml" --limit galaxyserver -e "mode_update=false" -e "mode_backup=false" --ask-vault-pass
```

### Run with Cleanup and Debug (Using a Vault Password File)
```bash
ansible-playbook -i /path/to/your/inventory/servers.tmp "$(pkgmgr path cymais)playbook.servers.yml" --limit galaxyserver -e "mode_update=false" -e "mode_backup=false" -e "mode_cleanup=true" -e "enable_debug=true" -v --vault-password-file /path/to/your/vault_pass.txt
```

---

## Using a Password File

To avoid entering your vault password interactively every time, use the `--vault-password-file` option:
```bash
--vault-password-file /path/to/your/vault_pass.txt
```
Ensure the vault password file is stored securely.

---

## Final Notes
- **Combining Modes:**  
  The different modes (reset, test, update, backup, cleanup) can be combined by passing extra variables (using `-e`) on the command line. This flexibility allows you to tailor the playbook run to your current needs.

- **Debugging:**  
  If you need more verbose output or troubleshooting information, add the `-v` (or `-vvv`) option when running the playbook.

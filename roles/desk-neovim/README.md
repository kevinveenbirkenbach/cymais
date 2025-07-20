# Desk-neovim Role for Ansible

## Overview
This role automates the installation of neovim, a CLI text editor, on Pacman‑based systems. It uses the `community.general.pacman` module to ensure the editor is installed and up to date.

## Requirements
- Ansible 2.9 or higher  
- Access to the Pacman package manager (e.g., Arch Linux and derivatives)

## Role Variables
No additional role variables are required; this role solely manages the installation of the editor.

## Dependencies
None.

## Example Playbook
```yaml
- hosts: all
  roles:
    - desk-neovim
```

## Further Resources
- Official neovim documentation: 
  https://neovim.io/

## Contributing
Contributions are welcome! Please follow standard Ansible role conventions and best practices.

## Other Resources
For more context on this role and its development, see the related ChatGPT conversation.

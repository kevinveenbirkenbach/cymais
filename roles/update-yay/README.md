# Ansible Role: update-yay

This Ansible role is designed for updating AUR packages on Arch Linux systems using `yay`. It automates the process of upgrading AUR packages, ensuring that your system stays up-to-date with the latest versions available in the Arch User Repository (AUR).

## Requirements

The role requires that `yay` (Yet Another Yaourt) - an AUR helper - is already installed on the system. If `yay` is not installed, the role `system-aur-helper` should handle its installation.

## Role Dependencies

- `system-aur-helper`: This dependency is essential for ensuring that `yay` is available on the system. If `yay` is not installed, this role will manage its installation.

## Role Variables

There are no specific variables that need to be defined by the user for this role. The role utilizes the `kewlfft.aur.aur` module with predefined parameters to manage AUR packages.

## Role Tasks

- **Upgrade AUR Packages**: The main task of this role is to upgrade the system using `yay`, focusing solely on AUR packages. This task does not require elevated privileges (become: false).

## Example Playbook

Here's an example of how to include the `update-yay` role in your playbook:

```yaml
- hosts: all
  roles:
    - role: update-yay
```

## Author Information

This role was created by Kevin Veen-Birkenbach.
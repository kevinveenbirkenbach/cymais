# PC-Security-Tools Role

## 📌 Overview
This README document is for the `pc-security-tools` role, a part of the `cymais` repository. This role is designed to equip personal computers with essential tools for enhancing data security and privacy.

## Role Tasks
The `main.yml` file within the `pc-security-tools` role encompasses tasks for installing key security software:

1. **Install Security Tools**:
   - Utilizes the `community.general.pacman` module to install a range of security tools, including:
     - `ecryptfs-utils`: Utilities for the enterprise cryptographic filesystem for Linux.
     - `encfs`: An encrypted filesystem that runs in userspace.
     - `keepassxc`: A free and open-source password manager that securely stores passwords and other sensitive data.

## Purpose and Usage
The `pc-security-tools` role is crucial for users who prioritize data security and privacy. It provides tools for encrypting files and directories, ensuring that sensitive data is protected. KeePassXC is particularly useful for managing passwords securely, an essential aspect of personal cybersecurity.

## Prerequisites
- **Ansible**: Must be installed on your system to run this role.
- **Arch Linux-based System**: Since the role uses the `pacman` package manager, it's best suited for Arch Linux or similar distributions.

## Running the Role
To use this role:
1. Clone the `cymais` repository.
2. Navigate to the `roles/pc-security-tools` directory.
3. Run the role using Ansible, making sure you have the necessary permissions for software installation.

## Customization
This role can be customized by adding or removing security-related software packages in the `main.yml` file, depending on your specific security needs or preferences.

## Support and Contributions
For support, feedback, or contributions, such as adding more security tools or enhancing the existing setup, please open an issue or submit a pull request in the `cymais` repository. Contributions that improve the security tools setup and user experience are highly encouraged.
# Administrator User

## Description

This role creates a dedicated administrator user for local administrative tasks. The administrator account is configured to require a password when executing [sudo](https://en.wikipedia.org/wiki/Sudo), ensuring secure privilege escalation. For security reasons, it is recommended to use this dedicated administrator user instead of the default root account. The role also sets up SSH-related configuration by copying an authorized_keys file from inventory data.

## 📌 Overview

Optimized for secure system management, this role performs the following:
- Creates an administrator user with a home directory.
- Configures proper permissions for the administrator’s home directory and associated scripts.
- Sets up an SSH authorized_keys file from inventory data (if available), leveraging [SSH](https://en.wikipedia.org/wiki/Secure_Shell) best practices.
- Grants [sudo](https://en.wikipedia.org/wiki/Sudo) privileges to the administrator user with password authentication using a dedicated sudoers file.

## Purpose

The primary purpose of this role is to provide a secure and dedicated administrator account solely for running local administration tasks. This approach minimizes security risks associated with using the root account and enforces best practices in user privilege management.

## Features

- **User Creation:** Establishes an administrator user with a home directory and generated SSH keys.
- **Home Directory Configuration:** Sets secure permissions on the administrator’s home directory and script folder.
- **SSH Authorized Keys:** Copies a preconfigured authorized_keys file for additional security.
- **Sudo Privileges:** Deploys a dedicated sudoers configuration to grant the administrator user [sudo](https://en.wikipedia.org/wiki/Sudo) rights with password prompt.
- **Modular Integration:** Integrates with common routines and roles to further enhance system security.

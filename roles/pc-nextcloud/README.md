# PC-Nextcloud Role

## Overview
This README details the `pc-nextcloud` role, part of the `computer-playbook` repository. This role focuses on setting up the Nextcloud client on personal computers and configuring directory synchronization.

## Role Variables
The `vars/main.yml` file defines key variables used in this role:
- `user_home_directory`: The home directory of the user, typically `/home/{{client_username}}/`.
- `cloud_directory`: The directory path for Nextcloud cloud storage, structured as `{{user_home_directory}}Clouds/{{cloud_fqdn}}/{{client_username}}/`.

## Role Tasks
The `main.yml` file in the `pc-nextcloud` role comprises the following tasks:

1. **Install Nextcloud-Client**:
   - Installs the Nextcloud desktop client using the `community.general.pacman` module.

2. **Link Homefolders to Cloud**:
   - Creates symbolic links from various user directories (like Templates, Documents, Videos, etc.) to corresponding folders in the Nextcloud cloud directory. This ensures synchronization of these folders with the user's Nextcloud account.

3. **Link Dump Folder**:
   - Specifically links a `Dump` folder in the user's home directory to the `InstantUpload` folder in the Nextcloud cloud directory for easy file dumping and syncing.

## Purpose and Usage
The `pc-nextcloud` role is designed for users who want to integrate Nextcloud, a cloud storage service, into their daily workflow. This role automates the installation of the Nextcloud client and the setup of directory synchronization, making files and documents easily accessible and syncable across devices.

## Prerequisites
- **Ansible**: Required for running this role.
- **Arch Linux-based System**: Since the role uses the `pacman` package manager, it's tailored for Arch Linux or similar distributions.

## Running the Role
To use this role:
1. Clone the `computer-playbook` repository.
2. Navigate to the `roles/pc-nextcloud` directory.
3. Ensure that the `client_username` and `cloud_fqdn` variables are correctly set to match your Nextcloud account details.
4. Execute the role using Ansible, ensuring appropriate permissions are available for installations and configurations.

## Customization
You can customize this role by modifying the variables in `vars/main.yml` and adjusting the directories in the linking tasks to suit your specific Nextcloud setup and preferences.

## Support and Contributions
For support, suggestions, or contributions, such as adding additional features or improving the setup, open an issue or submit a pull request in the `computer-playbook` repository. Contributions that enhance the integration and usability of Nextcloud on personal computers are highly welcome.
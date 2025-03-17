# PC-QBittorrent Role

## Overview
This README is for the `pc-qbittorrent` role within the `cymais` repository. This role is specifically crafted for installing qBittorrent, a popular open-source torrent client, on personal computers.

## Role Tasks
The `main.yml` file in the `pc-qbittorrent` role includes the following task:

1. **Install Torrent Software**:
   - This task uses the `kewlfft.aur.aur` module with `yay` as the AUR helper to install `qbittorrent`, a widely-used, free, and easy-to-use torrent client.

## Dependencies
This role depends on:
- **system-aur-helper**: Ensures that an Arch User Repository (AUR) helper is installed, which is necessary for installing packages like `qbittorrent` that are not available in the standard repositories.

## Purpose and Usage
The `pc-qbittorrent` role is tailored for users who require a reliable and user-friendly torrent client for downloading and sharing files via the BitTorrent protocol. qBittorrent is known for its balance of features, simplicity, and minimal impact on system resources.

## Prerequisites
- **Ansible**: Required for running this role.
- **Arch Linux-based System**: The role is designed with Arch Linux distributions in mind, leveraging AUR helpers for package installation.

## Running the Role
To utilize this role:
1. Clone the `cymais` repository.
2. Navigate to the `roles/pc-qbittorrent` directory.
3. Execute the role using Ansible, ensuring you have the required system permissions for package installation.

## Customization
This role is primarily focused on installing qBittorrent, but it can be customized to include additional configurations or related software packages as needed.

## Support and Contributions
For support, feedback, or contributions, such as enhancing the role or adding additional torrent-related functionality, please open an issue or submit a pull request in the `cymais` repository. Contributions that enhance the usability or features of qBittorrent within this role are highly appreciated.
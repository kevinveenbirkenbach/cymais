# PC-Spotify Role

## Overview
This README is for the `pc-spotify` role, part of the `computer-playbook` repository. This role is dedicated to installing Spotify, a popular digital music streaming service, on personal computers.

## Role Tasks
The `main.yml` file in the `pc-spotify` role includes the following task:

1. **Install Entertainment Software**:
   - Utilizes the `kewlfft.aur.aur` module with `yay` as the AUR helper to install `spotify`. Spotify offers streaming of millions of songs, podcasts, and videos from artists all around the world.

## Dependencies
This role depends on:
- **system-aur-helper**: Ensures that an Arch User Repository (AUR) helper is available, which is necessary for installing packages like `spotify` that are not available in the standard repositories.

## Purpose and Usage
The `pc-spotify` role is tailored for users who enjoy streaming music and wish to have Spotify readily available on their personal computer. This role simplifies the process of installing Spotify, making it accessible for listening to music, podcasts, and more.

## Prerequisites
- **Ansible**: Required for running this role.
- **Arch Linux-based System**: The role is designed for systems that use the `pacman` package manager and AUR helpers, typically found in Arch Linux distributions.

## Running the Role
To use this role:
1. Clone the `computer-playbook` repository.
2. Navigate to the `roles/pc-spotify` directory.
3. Execute the role using Ansible, ensuring you have the necessary system permissions for package installation.

## Customization
While this role is primarily focused on installing Spotify, it can be customized to include additional entertainment or media software as per user requirements.

## Support and Contributions
For support, feedback, or contributions, such as adding more features or enhancing the role, please open an issue or submit a pull request in the `computer-playbook` repository. Contributions that improve the entertainment software setup, including Spotify, are highly welcomed.
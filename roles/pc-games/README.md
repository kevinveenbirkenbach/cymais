# PC-Games Role

## Overview
This README is for the `pc-games` role, a part of the `computer-playbook` repository. This role is designed to install a variety of popular open-source and freely available games on personal computers.

## Role Contents
The `main.yml` file within the `pc-games` role automates the installation of several gaming titles using the `community.general.pacman` module. The games included are:

1. **Install Gaming Software**:
   - `0ad`: A free, open-source, historical real-time strategy (RTS) game.
   - `warzone2100`: A 3D RTS game set in a post-apocalyptic future.
   - `supertuxkart`: A free 3D kart racing game.
   - `gnuchess`: The GNU chess program.
   - `sauerbraten`: A first-person shooter game.
   - `minetest`: An open-source voxel game engine with easy modding and game creation.
   - `mari0`: A crossover between Super Mario and Portal.
   - `retroarch`: A frontend for emulators, game engines, and media players.
   - `retroarch-assets-xmb`: XMB menu assets for RetroArch.
   - `retroarch-assets-ozone`: Ozone menu assets for RetroArch.

## Purpose and Usage
The `pc-games` role is perfect for gamers who wish to have a variety of gaming experiences on their personal computer. It includes a range of games from different genres, providing options for players with diverse interests. The role is also suitable for setting up a gaming environment on new systems or restoring a collection of games after a system refresh.

## Prerequisites
- **Ansible**: You must have Ansible installed on your system to use this role.
- **Arch Linux-based System**: This role uses the `pacman` package manager, indicating it is designed for Arch Linux or similar distributions.

## Running the Role
To utilize this role:
1. Clone the `computer-playbook` repository.
2. Navigate to the `roles/pc-games` directory.
3. Execute the role using Ansible, ensuring you have the necessary permissions for software installation.

## Customization
You can customize this role by adding or removing games in the `main.yml` file based on your preferences or the requirements of your system.

## Support and Contributions
For support, feedback, or contributions, such as adding more games or enhancing the setup process, please open an issue or submit a pull request in the `computer-playbook` repository. Contributions that expand the gaming options or improve the installation process are highly welcomed.
# PC-Designer-Tools Role

## Overview
This README is associated with the `pc-designer-tools` role, part of the `cymais` repository. This role focuses on setting up a suite of essential design tools on personal computers, catering specifically to the needs of graphic designers, illustrators, and digital artists.

## Role Contents
The `main.yml` file in the `pc-designer-tools` role encompasses tasks for installing popular design software:

1. **Install Designer Tools**: This task uses the `community.general.pacman` module to install:
   - `gimp`: A free and open-source raster graphics editor, used for image retouching and editing, free-form drawing, converting between different image formats, and more specialized tasks.
   - `blender`: A free and open-source 3D creation suite supporting the entirety of the 3D pipeline—modeling, rigging, animation, simulation, rendering, compositing, and motion tracking, even video editing and game creation.

2. **Install drawio**: A separate task that uses the `kewlfft.aur.aur` module (with `yay` as the helper) to install `drawio-desktop`, a diagram software used for creating a wide range of diagrams and flowcharts.

## Dependencies
This role depends on:
- **system-aur-helper**: Ensures that an AUR (Arch User Repository) helper is available, which is necessary for installing packages like `drawio-desktop` that are not in the standard repositories.

## Purpose and Usage
The `pc-designer-tools` role is intended for users who require a robust set of tools for graphic design, 3D modeling, and diagram creation. It simplifies the process of setting up a comprehensive design environment on Arch Linux-based systems.

## Prerequisites
- **Ansible**: Required for running this role.
- **Arch Linux-based System**: As the role uses `pacman` and AUR helpers, it is tailored for Arch Linux or similar distributions.

## Running the Role
To use this role:
1. Clone the `cymais` repository.
2. Navigate to the `roles/pc-designer-tools` directory.
3. Execute the role using Ansible, ensuring you have the necessary permissions for software installation.

## Customization
This role can be customized by adding or removing software packages in the `main.yml` file to match the specific needs of the user.

## Support and Contributions
For support, feedback, or contributions, such as adding more tools or improving the existing setup, please open an issue or submit a pull request in the `cymais` repository. Contributions that enhance the role for designers are greatly appreciated.
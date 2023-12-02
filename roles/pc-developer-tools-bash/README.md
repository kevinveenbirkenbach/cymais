# PC-Developer-Tools-Bash Role

## Overview
This README accompanies the `pc-developer-tools-bash` role within the `cymais` repository. This role is dedicated to equipping personal computers with essential tools for Bash scripting and development.

## Role Contents
The `main.yml` file under the `pc-developer-tools-bash` role includes tasks focused on installing Bash development tools:

1. **Install Bash Developer Tools**:
   - This task leverages the `community.general.pacman` module to install:
     - `shellcheck`: A static analysis tool for shell scripts, which helps in identifying and correcting common errors or issues in Bash scripts.

## Dependencies
This role is dependent on:
- **pc-developer-tools**: Ensures that foundational developer tools are in place, providing a base environment for further specialized toolsets like Bash development tools.

## Purpose and Usage
The `pc-developer-tools-bash` role is specifically tailored for developers who frequently work with Bash scripting. ShellCheck, the main tool installed by this role, is invaluable for writing robust, error-free shell scripts. This role is ideal for system administrators, DevOps professionals, and anyone involved in script-based automation or Linux-based development.

## Prerequisites
- **Ansible**: You need to have Ansible installed on your system to use this role.
- **Arch Linux-based System**: The role utilizes `pacman`, thus it is best suited for Arch Linux or similar distributions.

## Running the Role
To execute this role:
1. Clone the `cymais` repository to your machine.
2. Navigate to the `roles/pc-developer-tools-bash` directory within the repository.
3. Run the role using Ansible, ensuring you have the necessary permissions to install software packages.

## Customization
The role can be customized by adding additional Bash development tools or utilities as per the user's requirements in the `main.yml` file.

## Support and Contributions
For support, feedback, or contributions (like adding more tools relevant to Bash development or enhancing the setup), please open an issue or submit a pull request in the `cymais` repository. Contributions that improve the Bash development environment are highly appreciated.
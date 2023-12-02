# PC-Git Role

## Overview
Welcome to the `pc-git` role documentation, part of the `computer-playbook` repository. This role is focused on setting up Git, a widely-used version control system, on personal computers. The role includes tasks for installing Git and configuring global user details.

## Role Tasks
The `main.yml` file in the `pc-git` role consists of the following key tasks:

1. **Set Git User Email**: Uses the `ansible.builtin.shell` module to set the global Git user email to a specified value (`{{user_email}}`).

2. **Set Git User Name**: Similar to the above, this task sets the global Git user name (`{{user_full_name}}`) using the `ansible.builtin.shell` module.

3. **Install Git**: Employs the `community.general.pacman` module to install the Git package, ensuring it's present on the system.

## Purpose and Usage
The `pc-git` role is essential for developers, IT professionals, and anyone who needs to utilize version control for their projects. It automates the installation of Git and the initial configuration of user identity, which is crucial for committing changes and collaborating on projects using Git.

## Prerequisites
- **Ansible**: Must be installed on your system to use this role.
- **Arch Linux-based System**: This role uses the `pacman` package manager, making it suitable for Arch Linux or similar distributions.

## Running the Role
To use this role:
1. Clone the `computer-playbook` repository.
2. Navigate to the `roles/pc-git` directory.
3. Make sure to define the `user_email` and `user_full_name` variables before running the role.
4. Execute the role using Ansible, ensuring you have the required permissions for software installation and configuration.

## Customization
You can customize this role by modifying the variables for user email and name or by adding additional Git configuration tasks as needed.

## Support and Contributions
For support, feedback, or contributions to this role, such as adding more Git-related configurations or tools, please open an issue or submit a pull request in the `computer-playbook` repository. Contributions that enhance Git setup and configuration are highly encouraged.
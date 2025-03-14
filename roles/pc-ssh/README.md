# PC-SSH Role

## 📌 Overview
Welcome to the `pc-ssh` role, a critical component of the `cymais` repository. This role is dedicated to setting up SSH (Secure Shell) on the client side, facilitating secure access to remote servers.

## Role Description
The `pc-ssh` role includes tasks to pull and update SSH configuration from a specified repository and handle potential errors:

1. **Pull SSH Repository**: 
   - Clones or updates the SSH configuration from a given repository (`{{ssh_configuration_repository}}`) into the `$HOME/.ssh` directory. This task ensures that your SSH configuration is synchronized with the specified repository.

2. **Warn if Repo is Not Reachable**:
   - Displays a warning message if the SSH configuration repository is not reachable, indicating potential issues with the repository's availability or the network connection.

## Dependencies
This role depends on:
- **pc-git**: Ensures that Git is installed, which is necessary for cloning and updating the SSH configuration repository.

## Purpose and Usage
The `pc-ssh` role is designed for users who require SSH access to remote servers, such as developers, system administrators, or IT professionals. By automating the SSH configuration process, this role streamlines the setup and ensures a consistent and secure SSH environment.

## Prerequisites
- **Ansible**: Must be installed to run this role.
- **Git**: Required for cloning and updating the SSH configuration repository.
- **Arch Linux-based System**: While not explicitly stated, the role's compatibility with specific systems depends on the dependencies and the overall playbook configuration.

## Running the Role
To use this role:
1. Clone the `cymais` repository.
2. Navigate to the `roles/pc-ssh` directory.
3. Define the `ssh_configuration_repository` variable with the URL of your SSH configuration repository.
4. Run the role using Ansible, ensuring you have the necessary permissions for executing the tasks.

## Customization
You can customize this role by modifying the SSH configuration repository URL or by adding additional SSH-related tasks as needed.

## Support and Contributions
For support, feedback, or contributions, such as enhancing the SSH setup or adding more features, please open an issue or submit a pull request in the `cymais` repository. Contributions that improve SSH configuration and usage are highly encouraged.
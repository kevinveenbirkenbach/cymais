# PC-Gnome Role

## Overview
Welcome to the `pc-gnome` role, a key part of the `computer-playbook` repository. This role is dedicated to setting up and configuring the GNOME desktop environment on personal computers.

## Role Details
The `pc-gnome` role includes several tasks for installing GNOME software, managing GNOME extensions, and customizing the GNOME desktop experience:

1. **Install Gnome Software**:
   - Installs essential GNOME packages such as `gnome-shell-extensions`, `gnome-shell-extension-desktop-icons-ng`, and `gnome-terminal` using the `community.general.pacman` module.

2. **GNOME Activate Extensions**:
   - Enables user extensions in GNOME using the `gsettings` command.

3. **GNOME Set Favorite Apps**:
   - Customizes the favorite applications on the GNOME shell using the `gsettings` command and the `{{favorite_apps}}` variable.

4. **Pull CLI GNOME Extension Manager Script**:
   - Clones or updates the CLI GNOME Extension Manager script from a Git repository.

5. **Warn if Repo is Not Reachable**:
   - Displays a warning message if the repository for the CLI GNOME Extension Manager script is not reachable.

6. **Execute CLI GNOME Extension Manager Script**:
   - Runs the CLI GNOME Extension Manager script to manage GNOME extensions based on the `{{gnome_extensions}}` variable.

## Further Information
For additional details on managing GNOME extensions via command line, visit [Ask Ubuntu](https://askubuntu.com/questions/1029376/how-do-i-enable-and-disable-gnome-extensions-from-the-command-line).

## Dependencies
This role depends on:
- **pc-git**: Ensures Git is installed for cloning repositories.
- **pc-caffeine**: A supplementary role that may include tools or configurations complementing the GNOME setup.

## Purpose and Usage
The `pc-gnome` role is ideal for users who prefer the GNOME desktop environment and wish to automate its setup and customization. It's especially useful for setting up a new system or reconfiguring GNOME after a system update.

## Prerequisites
- **Ansible**: Must be installed to use this role.
- **Arch Linux-based System**: The role uses the `pacman` package manager, indicating it's designed for Arch Linux or similar distributions.

## Running the Role
To use this role:
1. Clone the `computer-playbook` repository.
2. Navigate to the `roles/pc-gnome` directory.
3. Run the role using Ansible, ensuring you have the necessary permissions for installations and configurations.

## Customization
You can customize this role by modifying the GNOME software packages, favorite apps, and GNOME extensions in the respective tasks.

## Support and Contributions
For support, feedback, or contributions, such as adding more GNOME-related configurations or tools, open an issue or submit a pull request in the `computer-playbook` repository. Contributions that enhance the GNOME environment setup are highly encouraged.
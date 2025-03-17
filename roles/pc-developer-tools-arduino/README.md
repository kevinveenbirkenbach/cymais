# PC-Developer-Tools-Arduino Role

## Overview
This README file is for the `pc-developer-tools-arduino` role, a specialized component of the `cymais` repository. This role is specifically crafted for setting up Arduino development tools on personal computers.

## Role Details
The `main.yml` file in the `pc-developer-tools-arduino` role encompasses tasks crucial for Arduino developers:

1. **Install Arduino Developer Tools**:
   - This task employs the `community.general.pacman` module to install:
     - `arduino`: The Arduino IDE, which is an open-source electronics platform based on easy-to-use hardware and software.
     - `arduino-docs`: Documentation for Arduino, providing essential information for development.

2. **Adding User to Relevant Arduino Usergroups**:
   - This task modifies the user (specified by `{{client_username}}`) to be added to the `uucp` and `lock` groups, which is necessary for accessing serial ports on Linux systems.

## Dependencies
The role depends on:
- **pc-developer-tools**: Ensures that base developer tools, including code editors and related software, are installed and configured.

## Purpose and Usage
The `pc-developer-tools-arduino` role is tailored for developers and hobbyists who work with Arduino boards and need a reliable and efficient setup for their development environment. This role simplifies the process of installing and configuring the Arduino IDE and associated documentation, along with setting up necessary user permissions.

## Prerequisites
- **Ansible**: Required for executing this role.
- **Arch Linux-based System**: The role uses `pacman`, indicating it is designed for Arch Linux-based distributions.

## Running the Role
To utilize this role:
1. Clone the `cymais` repository.
2. Navigate to the `roles/pc-developer-tools-arduino` directory.
3. Execute the role using Ansible, ensuring you replace `{{client_username}}` with the actual username and have the necessary system permissions.

## Customization
This role can be customized to include additional Arduino-related packages or tools, depending on the user's requirements.

## Support and Contributions
For support, suggestions, or contributions (like adding more Arduino-related tools or improving the setup), please raise an issue or submit a pull request in the `cymais` repository. Contributions that enhance the Arduino development environment setup are highly encouraged.
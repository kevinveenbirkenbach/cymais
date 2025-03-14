# PC-Developer-Tools Role

## 📌 Overview
This README document is for the `pc-developer-tools` role within the `cymais` repository. The role is designed to streamline the setup of essential development tools on personal computers, particularly for software development environments.

## Role Contents
The `main.yml` file under the `pc-developer-tools` role includes tasks focused on the installation of key development tools:

1. **Install Base Developer Tools**:
   - This task uses the `community.general.pacman` module to install:
     - `code`: Visual Studio Code (VS Code), a powerful and popular open-source code editor that is highly customizable and supports a wide range of programming languages.

## Dependencies
This role relies on:
- **pc-administrator-tools**: Ensures that core administrative tools are installed, which can be essential for various development tasks.

## Purpose and Usage
The `pc-developer-tools` role is tailored for developers who need a quick and efficient setup of a development environment on their personal computer. It is particularly useful for programmers, software engineers, and anyone involved in software development who prefers a streamlined and efficient workflow.

## Prerequisites
- **Ansible**: Required to run this role.
- **Arch Linux-based System**: The role is designed with the `pacman` package manager in mind, thus it is best suited for Arch Linux or similar distributions.

## Running the Role
To utilize this role:
1. Clone the `cymais` repository.
2. Navigate to the `roles/pc-developer-tools` directory.
3. Run the role using Ansible, making sure you have the necessary privileges for package installation.

## Customization
Users can customize this role by adding more development tools or editors according to their specific needs in the `main.yml` file.

## Support and Contributions
For support, feedback, or contributions (such as adding more developer tools or enhancing the existing setup), please open an issue or submit a pull request in the `cymais` repository. Contributions that improve the development environment setup are highly welcomed.
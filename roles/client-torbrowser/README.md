# PC-TorBrowser Role

## Overview
This README document is for the `client-torbrowser` role, a crucial component of the `cymais` repository. This role is specifically designed for the installation and setup of Tor Browser on personal computers.

## Role Tasks
The `main.yml` file under the `client-torbrowser` role encompasses tasks for installing the Tor Browser:

1. **Install TorBrowser**:
   - Utilizes the `community.general.pacman` module to install:
     - `tor`: The core Tor service which facilitates anonymous communication.
     - `torbrowser-launcher`: A package for securely and easily launching the Tor Browser.

## Purpose and Usage
The `client-torbrowser` role is tailored for users who value privacy and anonymity online. The Tor Browser is a specialized web browser that provides enhanced privacy features, making it an essential tool for secure browsing and accessing the deep web.

## Prerequisites
- **Ansible**: Must be installed on your system to run this role.
- **Arch Linux-based System**: As the role uses the `pacman` package manager, it's best suited for Arch Linux or similar distributions.

## Running the Role
To use this role:
1. Clone the `cymais` repository.
2. Navigate to the `roles/client-torbrowser` directory.
3. Run the role using Ansible, ensuring you have the necessary permissions for software installation.

## Customization
While this role primarily focuses on installing Tor and the Tor Browser Launcher, you can customize it to include additional privacy-focused tools or configurations based on your needs.

## Support and Contributions
For support, feedback, or contributions, such as enhancing the role with more privacy tools or improving the installation process, please open an issue or submit a pull request in the `cymais` repository. Contributions that enhance the privacy and security aspects of this role are highly encouraged.
# Employee

## Overview
This README document is for the `persona-employee` role, a component of the `cymais` repository. This role is designed to install a suite of office-related software on personal computers, providing a comprehensive set of tools for various office tasks.

## Role Tasks
The `main.yml` file within the `persona-employee` role comprises tasks for installing a range of office software:

1. **Install Office Software**:
   - The role utilizes the `community.general.pacman` module to install the following software packages:
     - `chromium`: A free and open-source web browser.
     - `thunderbird`: A free and open-source email client, news client, RSS, and chat client.
     - `calibre`: An e-book management software.
     - `retext`: A simple but powerful editor for Markdown and reStructuredText.

## Dependencies
This role depends on:
- **client-libreoffice**: Ensures that the LibreOffice suite, a comprehensive office package, is installed.
- **client-zoom**: Provides tools necessary for video conferencing, supplementing the office setup.

## Purpose and Usage
The `persona-employee` role is ideal for users who require a full-fledged office setup on their personal computers. It encompasses tools for web browsing, email management, e-book organization, and document editing, catering to a wide range of office and productivity needs.

## Prerequisites
- **Ansible**: Must be installed to use this role.
- **Arch Linux-based System**: As the role uses the `pacman` package manager, it's intended for systems based on Arch Linux or similar distributions.

## Running the Role
To utilize this role:
1. Clone the `cymais` repository.
2. Navigate to the `roles/persona-employee` directory.
3. Run the role using Ansible, ensuring you have the necessary permissions for software installation.

## Customization
This role can be customized by adding or removing software packages in the `main.yml` file, depending on your specific office and productivity needs.

## Support and Contributions
For support, feedback, or contributions, such as adding more office tools or enhancing the current setup, please open an issue or submit a pull request in the `cymais` repository. Contributions that improve the office and productivity environment are highly welcomed.
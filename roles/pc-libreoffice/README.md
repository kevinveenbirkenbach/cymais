# PC-LibreOffice Role

## Overview
This README is for the `pc-libreoffice` role, part of the `cymais` repository. This role focuses on installing LibreOffice, a powerful and free office suite, along with necessary fonts and language packages.

## Role Contents
The `main.yml` file under the `pc-libreoffice` role includes tasks for installing LibreOffice and its components:

1. **Install LibreOffice**:
   - Uses the `community.general.pacman` module to install:
     - `ttf-liberation`: A font package that includes Liberation fonts, often used in LibreOffice documents.
     - `libreoffice-still`: The stable version of the LibreOffice suite.

2. **Install LibreOffice Language Packages**:
   - Installs various language packs for LibreOffice, allowing for multi-language support. The languages to be installed are determined by the `{{libreoffice_languages}}` variable.

## Dependencies
This role depends on:
- **hunspell**: Ensures that Hunspell, a spell checker used by LibreOffice for many languages, is installed.

## Purpose and Usage
The `pc-libreoffice` role is ideal for users who need a comprehensive, free office suite for personal or professional use. It's particularly useful for setting up a new system or ensuring that all necessary office software is present and properly configured.

## Prerequisites
- **Ansible**: Must be installed to use this role.
- **Arch Linux-based System**: The role uses the `pacman` package manager, making it suitable for Arch Linux or similar distributions.

## Running the Role
To use this role:
1. Clone the `cymais` repository.
2. Navigate to the `roles/pc-libreoffice` directory.
3. Define the `libreoffice_languages` variable with the desired language codes.
4. Run the role using Ansible, ensuring you have the necessary permissions for software installation.

## Customization
You can customize this role by adjusting the `libreoffice_languages` variable to include the language packs you need, or by adding additional LibreOffice-related packages as required.

## Support and Contributions
For support, feedback, or contributions, such as adding more functionality or enhancing the existing setup, please open an issue or submit a pull request in the `cymais` repository. Contributions that improve the LibreOffice setup and user experience are highly welcomed.
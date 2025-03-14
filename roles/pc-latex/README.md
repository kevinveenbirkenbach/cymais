# LaTeX Role

## 📌 Overview
Welcome to the LaTeX role within the `cymais` repository. It focuses on setting up a comprehensive LaTeX environment on Arch Linux-based systems, catering to the needs of users who require an advanced document preparation system.

## Role Contents
The `main.yml` file in this role automates the installation of key LaTeX packages:

1. **Install LaTeX Software**: This task uses the `community.general.pacman` module to install a range of LaTeX packages, ensuring a robust setup for LaTeX users. The packages include:
   - `texlive-pc-latexextra`: Offers additional LaTeX packages.
   - `texlive-lang`: Provides language support.
   - `texlive-langextra`: Includes extra language packs.
   - `texlive-fontsextra`: Adds a comprehensive collection of fonts.
   - `texlive-most`: Ensures a broad coverage of LaTeX components.

## Purpose and Usage
The LaTeX role is designed to streamline the installation of LaTeX on personal computers, particularly for users engaged in producing academic, scientific, or technical documentation. It is an essential tool for anyone who requires a full-fledged LaTeX environment for their documentation needs.

## Additional Information
For an extensive list of available LaTeX packages and customization options, you can refer to the [TeX Live on ArchWiki](https://wiki.archlinux.org/title/TeX_Live).

## Prerequisites
- **Ansible**: You must have Ansible installed on your system to utilize this role.
- **Arch Linux-based Systems**: Since this role uses the `pacman` package manager, it is tailored for Arch Linux or similar distributions.

## Running the Role
To execute this role:
1. Ensure the `cymais` repository is cloned to your system.
2. Navigate to the `roles/pc-latex` directory within the repository.
3. Run the role using the appropriate Ansible commands.

## Customization
You can customize this role by adjusting the list of LaTeX packages in `main.yml` to meet your specific needs.

## Support and Contributions
For support, feedback, or contributions, feel free to open an issue or a pull request in the `cymais` repository. Contributions that enhance or extend the role's capabilities are always welcome.
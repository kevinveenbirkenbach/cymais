# Git

## Description

This role installs and configures Git on the target system using the Pacman package manager (via the community.general.pacman module). In addition, it configures Git for the user by installing a custom git configuration using the [git-configurator](https://github.com/kevinveenbirkenbach/git-configurator) tool. The role ensures that Git is installed and that the configuration tasks are run only once per host.

## Purpose

The purpose of this role is to automate the installation and configuration of Git for personal computers. By leveraging a custom git-configurator, it sets up essential Git settings such as merge options, rebase preferences, user information, and GPG signing, ensuring a consistent environment for version control operations.

## Features

- **Automated Git Installation:** Installs Git using Pacman.
- **Custom Git Configuration:** Invokes the git-configurator tool to merge user-specific configuration options.
- **Idempotent Task Execution:** Uses host-level run-once artifacts to ensure that configuration tasks are executed only once per host.
- **Integration:** Works alongside the pkgmgr role to streamline overall system setup.

## Credits

Developed and maintained by **Kevin Veen-Birkenbach**.  
Learn more at [www.veen.world](https://www.veen.world)  
For Git configuration details, see [git-configurator on GitHub](https://github.com/kevinveenbirkenbach/git-configurator).

License: [CyMaIS NonCommercial License (CNCL)](https://s.veen.world/cncl)

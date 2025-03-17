# User

## Description

This role executes tasks that are relevant for all users by configuring essential shell files. It deploys customized templates for [`.bashrc`](https://wiki.archlinux.org/title/Bash#Startup_files) and [`.bash_profile`](https://wiki.archlinux.org/title/Bash#Login_shells) for any specified user. This ensures a consistent and enhanced shell environment across the system.

## Overview

Optimized for modular configuration, this role uses Jinja2 templates to create:
- A customized [`.bashrc`](https://wiki.archlinux.org/title/Bash#Startup_files) that sets up a dynamic welcome message, system information, and useful aliases.
- A standardized [`.bash_profile`](https://wiki.archlinux.org/title/Bash#Login_shells) that sources the `.bashrc` to ensure consistent behavior upon login.

The role adapts its file paths based on the target user (e.g. the [root user](https://en.wikipedia.org/wiki/Superuser) or a standard user), ensuring proper ownership and permissions.

## Purpose

The primary purpose of this role is to establish a consistent and informative shell environment for all users. By standardizing shell configuration, it helps improve usability and system management through clear and structured output upon login.

## Features

- **Shell Configuration:** Deploys customized [`.bashrc`](https://wiki.archlinux.org/title/Bash#Startup_files) and [`.bash_profile`](https://wiki.archlinux.org/title/Bash#Login_shells) files.
- **Dynamic Content:** Displays system information, load averages, memory usage, disk usage, CPU details, and top processes upon login.
- **User-Specific Customization:** Adapts file locations and ownership based on the target user.
- **Enhanced Usability:** Sets color-coded prompts and aliases for a better command-line experience.

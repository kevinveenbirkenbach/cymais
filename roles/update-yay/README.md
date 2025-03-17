# Update yay

## Description

This role updates AUR packages on Arch Linux systems using [yay](https://wiki.archlinux.org/title/Yay). It automates the process of upgrading AUR packages, ensuring that your system stays current with the latest software available in the Arch User Repository.

## Overview

The role performs the following:
- Checks if the [yay](https://wiki.archlinux.org/title/Yay) AUR helper is installed.
- Upgrades AUR packages using the `kewlfft.aur.aur` module with yay.
- Works exclusively on Arch Linux systems.

## Purpose

The primary purpose of this role is to ensure that AUR packages on Arch Linux are updated automatically. This helps maintain system stability and ensures that the latest features and fixes from the AUR are applied.

## Features

- **AUR Package Upgrades:** Uses yay to upgrade AUR packages.
- **Conditional Execution:** Only runs if yay is installed on the system.
- **Arch Linux Focused:** Specifically designed for Arch Linux systems.
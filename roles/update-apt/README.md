# Update Debian-based Systems

## Description

This role updates packages on Debian-based systems. It refreshes the apt cache and performs a distribution upgrade to ensure all packages are at their latest version.

## Overview

Designed for Debian and Ubuntu systems, this role:
- Updates the package cache using apt.
- Upgrades all packages to their latest available versions.
- Notes that full upgrades must be performed manually on non–rolling release systems.

## Purpose

The role is intended to keep Debian-based systems up-to-date by automating the package update process, ensuring that security patches and software improvements are applied promptly.

## Features

- **Apt Cache Refresh:** Updates the package index.
- **Distribution Upgrade:** Performs a dist-upgrade to update all installed packages.
- **Debian-Specific:** Tailored for Debian-based distributions.

# Docker 🐳

## Description

This Ansible role installs and manages Docker on Arch Linux systems. It ensures that Docker and Docker Compose are available, configured, and ready to run containerized workloads, while enabling seamless integration with system roles and administrative tasks.
Checkout the [administration reference](./Administration.md) for volume cleanup, container resets, and Docker network recovery.

## Overview

Tailored for Arch Linux, this role handles the installation of Docker and Docker Compose using the system’s package manager. It sets up a secure environment for managing Compose instances and ensures the Docker service is properly enabled and restarted. In addition, the role flags its state so that dependent roles can execute conditionally.

## Purpose

The purpose of this role is to automate the provisioning of Docker environments in a consistent and maintainable way. It reduces manual setup steps and enables clean integration with other infrastructure roles, making it ideal for production or homelab deployments.

## Features

- **Installs Docker & Docker Compose:** Uses `pacman` to install necessary packages.
- **Service Management:** Automatically enables and restarts the Docker service.
- **Secure Directory Creation:** Creates a secure location for Docker Compose instance files.
- **Run-once Setup Logic:** Ensures idempotent execution by controlling task flow with internal flags.
- **System Role Integration:** Sets internal state (`docker_enabled`) for use by other CyMaIS roles.

## Credits 📝

Developed and maintained by **Kevin Veen-Birkenbach**.  
Learn more at [www.veen.world](https://www.veen.world)

Part of the [CyMaIS Project](https://github.com/kevinveenbirkenbach/cymais)  
License: [CyMaIS NonCommercial License (CNCL)](https://s.veen.world/cncl)
# Central Database

## Description

This Ansible role provisions a centralized database system in your Docker Compose environment. It supports both MariaDB and PostgreSQL, providing a robust, scalable, and low-maintenance database solution. Whether you're consolidating your application's data or creating a dedicated central storage, this role simplifies setup and integration.

## Overview

Tailored for environments that require a central data repository, this role:
- Loads necessary database variables defined in [vars/database.yml](./vars/database.yml).
- Generates an environment file based on the chosen database engine.
- Integrates seamlessly with Docker Compose to deploy a centralized database container (if enabled).

## Purpose

The role's purpose is to automate the provisioning and configuration of a centralized database service. This not only reduces manual setup but also ensures consistent, reliable deployment across production and homelab environments.

## Features

- **Supports Multiple Engines:** Easily switch between MariaDB and PostgreSQL.
- **Centralized Data Management:** Improves data consistency and security.
- **Docker Compose Integration:** Automates container setup and configuration.
- **Simplified Variable Management:** Preconfigured templates minimize manual intervention.

## Credits 📝

Developed and maintained by **Kevin Veen-Birkenbach**.  
Learn more at [www.veen.world](https://www.veen.world)  
Part of the [Infinito.Nexus Project](https://github.com/kevinveenbirkenbach/infinito-nexus)  
License: [Infinito.Nexus NonCommercial License (CNCL)](https://s.veen.world/cncl)

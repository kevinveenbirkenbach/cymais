# OpenProject 🧭

## Description

This role deploys [OpenProject](https://www.openproject.org/) using Docker Compose and provides a fully integrated experience for project collaboration with optional support for LDAP authentication and SMTP email delivery. Ideal for teams or individuals who want to get started with OpenProject quickly without manually setting up infrastructure.

## Overview

Designed for simplicity, this role automates everything needed to run OpenProject in a containerized environment. It configures essential services such as the application itself, a PostgreSQL database, reverse proxy, and optional LDAP integration for identity management.

## Purpose

The purpose of this role is to reduce the complexity of setting up OpenProject with modern production-ready defaults. By combining Docker Compose and Ansible automation, it enables a hands-off setup for both small teams and larger internal infrastructures.

## Features

- 🐳 **Docker-First Deployment**: Uses Docker Compose to launch the entire OpenProject stack.
- 🔒 **LDAP Integration (optional)**: Automatically connects to your LDAP server for centralized authentication.
- 📬 **SMTP Configuration**: Sends notification emails via your own mail server.
- 🧩 **OIDC Ready**: Prepared to extend with OpenID Connect login (e.g., Keycloak).
- 🔄 **Plugin Support**: Supports custom plugin installation via a pluggable `Gemfile.plugins`.
- 🛠️ **Role-Oriented Architecture**: Easily integrates with your infrastructure (e.g., database, reverse proxy).

## Developer Notes

See the [Development.md](./Development.md) file for how to inspect and modify live settings inside the container, including full LDAP and SMTP configuration via the Rails console.

## Credits 📝

Developed and maintained by **Kevin Veen-Birkenbach**  
Learn more at [www.veen.world](https://www.veen.world)

Part of the [CyMaIS Project](https://github.com/kevinveenbirkenbach/cymais)  
License: [CyMaIS NonCommercial License (CNCL)](https://s.veen.world/cncl)
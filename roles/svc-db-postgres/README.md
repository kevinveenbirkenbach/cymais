# PostgreSQL

## Description

This Ansible role deploys and configures a PostgreSQL database in a Docker container using Docker Compose. It is designed to simplify database administration by automating the creation of networks, containers, and essential database tasks (such as database and user creation) for a secure and high-performance environment.

## Overview

Built for environments that demand reliability and ease of management, this role:
- Sets up a dedicated Docker network for PostgreSQL.
- Deploys a PostgreSQL container with secure configurations and automated healthchecks.
- Automates tasks like database creation, user setup, and privilege assignments to streamline your workflows.

## Purpose

The purpose of this role is to provide an effortless way to deploy a PostgreSQL database via Docker. It minimizes manual interventions while ensuring that your database is configured securely and reliably for both production and development scenarios.

## Features

- **Automated Deployment:** Installs PostgreSQL with minimal manual steps.
- **Robust Administration:** Automatically creates databases, users, and assigns privileges.
- **Enhanced Security:** The service is bound to `127.0.0.1:5432`, restricting access and enhancing security.
- **Seamless Docker Integration:** Works harmoniously with Docker Compose and other roles in your infrastructure.

## Credits 📝

Developed by **Kevin Veen-Birkenbach**.  
Discover more at [www.veen.world](https://www.veen.world)  
Part of the [Infinito.Nexus Project](https://github.com/kevinveenbirkenbach/infinito-nexus)  
License: [Infinito.Nexus NonCommercial License (CNCL)](https://s.veen.world/cncl)
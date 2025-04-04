# PgAdmin 🐳

## Description

This Ansible role deploys [pgAdmin](https://www.pgadmin.org/) in a secure Docker environment, with optional OAuth2 proxy support. It provides a full-featured web UI to manage PostgreSQL databases, making it ideal for both development and production use.

## Overview

The role provisions a containerized pgAdmin instance using Docker Compose. It allows integration with central PostgreSQL servers, and supports environment-specific settings via Ansible variables.

## Purpose

The purpose of this role is to offer a quick and configurable way to deploy pgAdmin with Docker, while keeping it secure through optional OAuth2 integration. It's built to fit seamlessly into CyMaIS-managed environments.

## Features

- **Docker Compose Integration:** Deploy pgAdmin with a templated Compose file.
- **OAuth2 Proxy Support:** Add authentication via an external OAuth2 provider.
- **Central DB Integration:** Easily connect to central PostgreSQL instances.
- **Customizable Settings:** Adjust container configuration via Ansible variables.
- **Healthchecks & Networking:** Includes built-in Docker healthchecks and Compose networks.

## Credits 📝

Developed and maintained by **Kevin Veen-Birkenbach**.  
Learn more at [www.veen.world](https://www.veen.world)

Part of the [CyMaIS Project](https://github.com/kevinveenbirkenbach/cymais)  
License: [CyMaIS NonCommercial License (CNCL)](https://s.veen.world/cncl)

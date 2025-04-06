# Taiga 🐳📋

## Description

This Ansible role deploys and configures the [Taiga](https://www.taiga.io/) project management platform using Docker. It supports core services like backend, frontend, events, and async processing — with optional integration for OpenID Connect (OIDC) authentication.

Designed for Arch Linux systems, it ensures consistent and modular setup of the entire Taiga stack, including database and proxy configuration. This role integrates with the CyMaIS infrastructure through conditional Docker Compose file generation and optional service dependencies.

## Overview

- Deploys Taiga using Docker and Docker Compose.
- Supports PostgreSQL and RabbitMQ as dependencies.
- Automatically integrates Nginx as a reverse proxy.
- Optionally enables OIDC via `taiga-contrib-openid-auth`.

## Purpose

The purpose of this role is to automate the provisioning of a complete, containerized Taiga environment in a secure, repeatable, and infrastructure-compliant way. It supports multiple deployment scenarios (internal tools, team collaboration, or homelab usage) and fits into a modular Ansible-based DevOps workflow.

## Features

- 🐳 **Docker-Based Deployment** – Uses `docker-compose` to orchestrate all services.
- 🔐 **Optional OpenID Connect Integration** – Conditionally enables Keycloak or other OIDC providers.
- 🔁 **Async and Event Support** – Includes `taiga-events` and `taiga-async`.
- 📨 **SMTP Email Support** – Supports both real and console email backends.
- 🧩 **Modular Role Integration** – Compatible with roles like `docker-central-database`, `nginx-domain-setup`, and `docker-repository-setup`.

## Credits 📝

Developed and maintained by **Kevin Veen-Birkenbach**  
Visit [veen.world](https://www.veen.world) for more information.  
Part of the [CyMaIS Project](https://github.com/kevinveenbirkenbach/cymais)  
License: [CyMaIS NonCommercial License (CNCL)](https://s.veen.world/cncl)
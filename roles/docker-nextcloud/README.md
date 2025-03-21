# Nextcloud

## Description

This Ansible role provisions a production-grade **Nextcloud** deployment using Docker Compose. It includes support for LDAP and OIDC authentication, Redis caching, secure configuration management, and declarative plugin control via `occ`. The setup is modular and integrates cleanly into larger infrastructure environments.

## Overview

The role ensures consistent deployments, full automation, and secure configuration injection into `config.php` using additive includes. Authentication is handled through LDAP and OIDC (e.g., via Keycloak), and backup/recovery operations are fully supported.

## Purpose

To automate the deployment of **secure, extensible, and production-ready Nextcloud instances** using Docker and Ansible.

## Features

- Dockerized Nextcloud (PHP-FPM, Nginx, Cron, Redis)
- Templated Nginx configuration (internal and external)
- Automated certificate and HTTPS proxy integration
- Healthcheck support
- Backup & recovery integration
- IAM & SOO
- Hundreds of integrated plugins

## Related Documentation

Here are all supporting documentation files within this role:

| Topic | Description |
|-------|-------------|
| [Applications](Applications.md) | SQL examples and debug notes for plugins like **Cospend** |
| [Architecture](Architecture.md) | Overview of architectural integrations |
| [Administration](Administration.md) | Manual operations like update, config edits, recovery |
| [Update](Update.md) | Step-by-step update and restore instructions |
| [OCC](OCC.md) | Nextcloud CLI usage guide (user management, config, maintenance) |
| [Database](Database.md) | Managing the database (local mode) |
| [IAM](IAM.md) | LDAP & OIDC Identity and Access Management |

## External Resources

- [Nextcloud Docker Documentation](https://github.com/nextcloud/docker)
- [Nextcloud Admin Manual](https://docs.nextcloud.com/server/latest/admin_manual/)
- [LDAP Integration Guide](https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/user_auth_ldap.html)
- [OIDC Login Plugin (pulsejet)](https://github.com/pulsejet/nextcloud-oidc-login)
- [Sociallogin Plugin (Official)](https://apps.nextcloud.com/apps/sociallogin)
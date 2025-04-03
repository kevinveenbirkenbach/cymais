# WordPress

## Description

This role deploys and manages a Docker-based [WordPress](http://wordpress.com/) instance, including support for multisite installations. It builds a custom WordPress image that installs msmtp (for email delivery) and configures PHP settings for uploads and email functionality.

For detailed administrative procedures (database access, container management, etc.), please refer to the [Administration Reference](./Administration.md).

## Overview

Tailored for Arch Linux environments using Docker, this role:
- **Custom Image Build:** Builds a Docker image for WordPress with msmtp installed to act as a sendmail replacement.
- **Multisite Support:** Configures WordPress to support multiple sites by integrating with external domain setup roles.
- **Centralized Database Management:** Leverages the docker-central-database role to ensure consistent database configuration.
- **Docker Compose Integration:** Uses Docker Compose templates for container orchestration and service management.

## Purpose

The role aims to automate the provisioning of a robust, scalable WordPress instance in a containerized environment while ensuring reliable email delivery through msmtp and streamlined multi-site management.

## Features

- **Custom WordPress Container:** Builds an image with msmtp and custom PHP settings.
- **Multisite Capabilities:** Configures settings and domains for multisite WordPress deployments.
- **Integrated Database Access:** Works in tandem with a central database role.
- **Seamless Docker Compose Deployment:** Provides templates for Docker Compose and environment configuration.
- **Administration Documentation:** See the [Administration Reference](./Administration.md) for tasks like database access, upgrades, and configuration updates.

## multiside
- https://multilingualpress.de/doku/wordpress-multisite-installieren-einrichten/
- https://pressable.com/knowledgebase/adding-or-changing-the-domain-on-a-wordpress-multisite/
- https://wpengine.com/support/how-to-change-a-multi-site-primary-domain/

## Credits

Developed and maintained by **Kevin Veen-Birkenbach**.  
Learn more at [www.veen.world](https://www.veen.world)

Part of the [CyMaIS Project](https://github.com/kevinveenbirkenbach/cymais)  
License: [CyMaIS NonCommercial License (CNCL)](https://s.veen.world/cncl)

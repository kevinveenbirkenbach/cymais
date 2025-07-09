# Administrator Guide

This guide is for **system administrators** who are deploying and managing CyMaIS infrastructure.

## Setting Up CyMaIS 🏗️
Follow these guides to install and configure CyMaIS:
- [Setup Guide](SETUP_GUIDE.md)
- [Configuration Guide](CONFIGURATION.md)
- [Deployment Guide](DEPLOY.md)

## Key Responsibilities 🔧
- **User Management** - Configure LDAP, Keycloak, and user permissions.
- **Security & Backups** - Set up `bkp-remote-to-local`, `bkp-data-to-usb`, and `core-security` roles.
- **Application Hosting** - Deploy services like `Nextcloud`, `Matrix`, `Gitea`, and more.
- **Networking & VPN** - Configure `WireGuard`, `OpenVPN`, and `Nginx Reverse Proxy`.

## Managing & Updating CyMaIS 🔄
- Regularly update services using `update-docker`, `update-pacman`, or `update-apt`.
- Monitor system health with `mon-bot-btrfs`, `mon-bot-webserver`, and `mon-bot-docker-container`.
- Automate system maintenance with `maint-lock`, `cleanup-backups-service`, and `maint-docker-restart`.

For more details, refer to the specific guides above.
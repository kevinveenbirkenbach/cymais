# Administrator Guide 🖥️

This guide is for **system administrators** who are deploying and managing CyMaIS infrastructure.

## Setting Up CyMaIS 🏗️
Follow these guides to install and configure CyMaIS:
- [Setup Guide](07_SETUP_GUIDE.md)
- [Configuration Guide](08_CONFIGURATION.md)
- [Deployment Guide](09_DEPLOY.md)

## Key Responsibilities 🔧
- **User Management** - Configure LDAP, Keycloak, and user permissions.
- **Security & Backups** - Set up `backup-remote-to-local`, `backup-data-to-usb`, and `system-security` roles.
- **Application Hosting** - Deploy services like `Nextcloud`, `Matrix`, `Gitea`, and more.
- **Networking & VPN** - Configure `WireGuard`, `OpenVPN`, and `Nginx Reverse Proxy`.

## Managing & Updating CyMaIS 🔄
- Regularly update services using `update-docker`, `update-pacman`, or `update-apt`.
- Monitor system health with `health-btrfs`, `health-nginx`, and `health-docker-container`.
- Automate system maintenance with `system-maintenance-lock`, `cleanup-backups-service`, and `restart-docker`.

For more details, refer to the specific guides above.
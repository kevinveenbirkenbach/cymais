# Nginx Certbot Automation

## 🔥 Description

This role automates the setup of an automatic [Let's Encrypt](https://letsencrypt.org/) certificate renewal system for Nginx using [Certbot](https://certbot.eff.org/). It ensures that SSL/TLS certificates are renewed seamlessly in the background and that Nginx reloads automatically after successful renewals.

## 📖 Overview

Optimized for Archlinux systems, this role installs the `certbot-nginx` package, configures a dedicated `systemd` service for certificate renewal, and integrates with a `gen-timer` to schedule periodic renewals. After a renewal, Nginx is reloaded to apply the updated certificates immediately.

### Key Features
- **Automatic Renewal:** Schedules unattended certificate renewals using gen-timers.
- **Seamless Nginx Reload:** Reloads the Nginx service automatically after successful renewals.
- **Systemd Integration:** Manages renewal operations reliably with `systemd` and `alert-compose`.
- **Quiet and Safe Operation:** Uses `--quiet` and `--agree-tos` flags to ensure non-interactive renewals.

## 🎯 Purpose

The Nginx Certbot Automation role ensures that Let's Encrypt SSL/TLS certificates stay valid without manual intervention. It enhances the security and reliability of web services by automating certificate lifecycle management.

## 🚀 Features

- **Certbot-Nginx Package Installation:** Installs required certbot plugins for Nginx.
- **Custom Systemd Service:** Configures a lightweight, dedicated renewal service.
- **Timer Setup:** Uses gen-timer to run certbot renewals periodically.
- **Failure Notification:** Integrated with `alert-compose` for alerting on failures.

## 🔗 Learn More

- [Certbot Official Website](https://certbot.eff.org/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Systemd (Wikipedia)](https://en.wikipedia.org/wiki/Systemd)
- [HTTPS (Wikipedia)](https://en.wikipedia.org/wiki/HTTPS)

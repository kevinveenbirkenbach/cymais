# Roles

This directory contains all of the Ansible roles used throughout the CyMaIS project. Roles are organized by function and prefixed accordingly.

For a complete list of role categories and detailed definitions, see:

- [Application Glossary](application_glosar.rst)  
- [Application Categories](application_categories.rst)

---

## Core & System

- **core-***  
  Fundamental system configuration (SSH, journald, sudo, etc.)

- **generic-***  
  Generic helpers and language/tool installers (e.g. `generic-git`, `generic-locales`, `generic-timer`)

- **desk-***  
  Desktop environment and application roles (e.g. `desk-gnome`, `utils-desk-browser`, `desk-libreoffice`)

---

## Webserver & HTTP

- **webserver-core**  
  Installs and configures the base Nginx server.

- **webserver-tls-***  
  Manages TLS certificates and renewal (formerly “https”).

- **webserver-proxy-***  
  Proxy and vhost orchestration roles (domain setup, OAuth2 proxy, etc.)

- **webserver-injector-***  
  HTML response modifiers: CSS, JS, Matomo tracking, iframe notifier.

- **webserver-composer**  
  Aggregates multiple sub-filters into one include for your vhost.

- **web-service-***  
  Static‐content servers (assets, HTML, legal pages, file hosting).

- **web-app-***  
  Application-specific Docker/Compose roles (e.g. GitLab, Nextcloud, Mastodon).

---

## Network

- **network-***  
  Network infrastructure (DNS records, WireGuard, Let’s Encrypt entrypoints).

- **service-***  
  Docker‐deployed services that aren’t “apps” (RDBMS, LDAP, Redis, OpenLDAP).

---

## Monitoring & Alerting

- **monitor-bot-***  
  “Bot”-style health checks with alerts via Telegram, email, etc.

- **monitor-core-***  
  Low-level system monitors (journalctl, Docker containers, disk space).

- **alert-***  
  Failure or status notification handlers (core, email, Telegram).

---

## Maintenance & Healing

- **maintenance-***  
  Periodic maintenance tasks (Btrfs balancing, swapfile management).

- **maintenance-docker-***  
  Automated recovery and restarts for Docker Compose workloads.

- **cleanup-***  
  Housekeeping tasks (old backups, certs, log rotation).

---

## Backup & Restore

- **backup-***  
  Local and remote backup strategies for files, Docker volumes, databases.

---

## Updates & Package Management

- **update-***  
  Keeps OS and language packages up to date (`update-apt`, `update-docker`, `update-pip`, etc.)

- **pkgmgr-***  
  Language or platform package managers (npm, pip, AUR helper).

---

## Users & Access

- **user-***  
  Creates user accounts and SSH keys.

- **user-administrator**, **user-root**  
  Specialized account configurations for privileged users.

---

> **Tip:** To find a role quickly, search for its prefix:  
> `core-`, `generic-`, `desk-`, `webserver-`, `web-service-`, `web-app-`,  
> `network-`, `service-`, `monitor-`, `alert-`, `maintenance-`, `cleanup-`,  
> `backup-`, `update-`, `pkgmgr-`, `user-`.

---

_For more details on which applications each role supports, see the [Application Categories](application_categories.rst) and the full [Application Glossary](application_glosar.rst)._  

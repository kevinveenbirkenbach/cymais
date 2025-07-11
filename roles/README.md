# Roles

This directory contains all of the Ansible roles used throughout the CyMaIS project. Roles are organized by function and prefixed accordingly.

For a complete list of role categories and detailed definitions, see:

- [Application Glossary](application_glosar.rst)  
- [Application Categories](application_categories.rst)

---

## Core & System

- **core-***  
  Fundamental system configuration (SSH, journald, sudo, etc.)

- **gen-***  
  Generic helpers and language/tool installers (e.g. `gen-git`, `gen-locales`, `sys-timer`)

- **desk-***  
  Desktop environment and application roles (e.g. `desk-gnome`, `desk-browser`, `desk-libreoffice`)

---

## Webserver & HTTP

- **srv-web-7-4-core**  
  Installs and configures the base Nginx server.

- **srv-web-6-6-tls-***  
  Manages TLS certificates and renewal (formerly “https”; e.g. `srv-web-6-6-tls-deploy`, `srv-web-6-6-tls-renew`).

- **srv-web-proxy-***  
  Proxy and vhost orchestration roles (domain setup, OAuth2 proxy, etc.)

- **srv-web-7-7-inj-***  
  HTML response modifiers: CSS, JS, Matomo tracking, iframe notifier.

- **srv-web-7-6-composer**  
  Aggregates multiple sub-filters into one include for your vhost.

- **web-svc-***  
  Static‐content servers (assets, HTML, legal pages, file hosting).

- **web-app-***  
  Application-specific Docker/Compose roles (e.g. GitLab, Nextcloud, Mastodon, Redis).

---

## Network

- **net-***  
  Network infrastructure (DNS records, Let’s Encrypt HTTP entrypoints, WireGuard, etc.)

- **svc-***  
  Docker-deployed services that aren’t “apps” (RDBMS, LDAP, Redis, OpenLDAP).

---

## Monitoring & Alerting

- **sys-hlth-***  
  “Bot”-style health checks (Btrfs, disk‐space, Docker, journalctl, CSP crawler, webserver) with alerts.

- **monitor-core-***  
  Low-level system monitors (journalctl, Docker containers, disk space, etc.)

- **sys-alm-***  
  Notification handlers for failures (core, email, Telegram).

---

## Maintenance & Healing

- **maint-***  
  Periodic maintenance tasks (Btrfs balancing, swapfile management, etc.)

- **maint-docker-***  
  Automated recovery and restarts for Docker Compose workloads.

- **sys-cln-***  
  Housekeeping tasks (old backups, expired certs, log rotation).

---

## Backup & Restore

- **sys-bkp-***  
  Local and remote backup strategies for files, Docker volumes, databases.

---

## Updates & Package Management

- **update-***  
  Keeps OS and language packages up to date (`update-apt`, `update-docker`, `update-pip`, etc.)

- **pkgmgr-***  
  Language or platform package managers (npm, pip, AUR helper, etc.)

---

## Users & Access

- **user-***  
  Creates user accounts and SSH keys.

- **user-administrator**, **user-root**  
  Specialized configurations for privileged users.

---

> **Tip:** To find a role quickly, search for its prefix:  
> `core-`, `gen-`, `desk-`, `srv-web-`, `web-svc-`, `web-app-`,  
> `net-`, `svc-`, `sys-hlth-`, `monitor-core-`, `sys-alm-`,  
> `maint-`, `maint-docker-`, `sys-cln-`, `sys-bkp-`, `update-`,  
> `pkgmgr-`, `user-`.

---

_For more details on which applications each role supports, see the [Application Categories](application_categories.rst) and the full [Application Glossary](application_glosar.rst)._  

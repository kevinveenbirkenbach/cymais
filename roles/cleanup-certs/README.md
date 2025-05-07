# Certbot Reaper

## Description

This Ansible role automates the process of detecting, revoking, and deleting unused Let's Encrypt certificates. It leverages the [`certreap`](https://github.com/kevinveenbirkenbach/certreap) tool to identify which certificates are no longer referenced by any active NGINX configuration and removes them accordingly.

## Overview

Optimized for Archlinux, this role installs the certificate cleanup tool, configures a systemd service, and sets up an optional recurring systemd timer for automatic cleanup. It integrates with dependent roles for timer scheduling and system notifications.

## Purpose

Certbot Reaper helps you maintain a clean and secure server environment by regularly removing obsolete SSL certificates. This prevents unnecessary renewal attempts, clutter, and potential security risks from stale certificates.

## Features

- **Certificate Cleanup Tool Installation:** Installs `certreap` using [pkgmgr](https://github.com/kevinveenbirkenbach/package-manager)
- **Systemd Service Configuration:** Deploys and manages `cleanup-certs.cymais.service`
- **Systemd Timer Scheduling:** Optional timer via the `systemd-timer` role
- **Smart Execution Logic:** Ensures idempotent configuration using a `run_once` flag

## License

This role is licensed under the [CyMaIS NonCommercial License (CNCL)](https://s.veen.world/cncl).  
Commercial use is not permitted without explicit permission.
# Cleanup Backups Timer

## Description

This role sets up a systemd timer to schedule the periodic cleanup of old backups. It leverages the cleanup-backups-service role to perform the actual cleanup operation.

## Overview

Optimized for automated maintenance, this role:
- Sets a fact for the service name.
- Integrates with the [systemd-timer](../systemd-timer/README.md) role to schedule cleanup-backups tasks at defined intervals.

## Purpose

The primary purpose of this role is to automate the scheduling of backup cleanup operations using a systemd timer, ensuring that backup storage remains within defined limits.

## Features

- **Timer Scheduling:** Configures a systemd timer to trigger the backup cleanup service.
- **Role Integration:** Works in conjunction with the cleanup-backups-service role.
- **Idempotency:** Ensures the timer tasks execute only once per playbook run.

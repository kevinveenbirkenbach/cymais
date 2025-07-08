# Docker Volume Backup Cleanup Role

## Description

This role cleans up failed Docker backups by pulling a [Git repository](https://github.com/kevinveenbirkenbach/cleanup-failed-docker-backups) that contains cleanup scripts and configuring a systemd service to execute them. It ensures that failed or incomplete backups are removed to free up disk space and maintain a healthy backup environment.

## Overview

Optimized for backup maintenance, this role:
- Clones the cleanup-failed-docker-backups repository.
- Configures a systemd service to run the cleanup script.
- Integrates with the [generic-timer](../generic-timer/README.md) role to schedule periodic cleanup.
- Works in conjunction with the backup-directory-validator role for additional verification.

## Purpose

The primary purpose of this role is to remove failed Docker backups automatically, thereby freeing disk space and preventing backup storage from becoming cluttered with incomplete data.

## Features

- **Repository Cloning:** Retrieves the latest cleanup scripts from a Git repository.
- **Service Configuration:** Sets up a systemd service to run the cleanup tasks.
- **Timer Integration:** Schedules periodic cleanup through a systemd timer.
- **Dependency Integration:** Works with backup-directory-validator to enhance backup integrity.
# Backup Directory Validator

## Description

This Ansible role pulls the [directory-validator](https://github.com/kevinveenbirkenbach/directory-validator.git) repository to a predefined location. It is used by the backup-docker-to-local and cleanup-failed-docker-backups roles to verify whether backups have been successfully created.

## 📌 Overview

The role retrieves the latest version of the directory-validator from its Git repository and installs it into the designated folder (configured via the `backup_directory_validator_folder` variable). A fact is set to ensure that the repository is pulled only once per playbook run.

## Purpose

The primary purpose of this role is to validate backup directories. By fetching the directory-validator tool, it enables dependent roles to assess the integrity and success of backup operations.

## Features

- **Git Repository Pull:** Automatically pulls the latest version of the directory-validator from Git.
- **Idempotent Execution:** Ensures that the repository is fetched only once per playbook run.
- **Backup Verification:** Serves as a validation step for other backup-related roles.
- **Configurable Destination:** The target folder is customizable via the `backup_directory_validator_folder` variable.

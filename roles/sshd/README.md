# SSHD

## Description

This role configures the SSH daemon ([sshd](https://man7.org/linux/man-pages/man5/sshd_config.5.html)) on the target system by deploying a templated configuration file. It ensures that secure and proper SSH settings are applied, reducing the risk of misconfiguration and potential lockout.

## 📌 Overview

Optimized for secure remote access, this role:
- Generates an SSH daemon configuration file from a Jinja2 template.
- Sets appropriate ownership and permissions on the configuration file.
- Notifies systemd to restart the SSH daemon when changes are made.

## Purpose

The primary purpose of this role is to establish a secure SSH environment by deploying a well-configured sshd_config file. This helps prevent unauthorized access and potential system lockouts, while ensuring that the SSH service runs smoothly.

## Features

- **SSH Configuration Deployment:** Creates an sshd_config file with best-practice settings.
- **Systemd Integration:** Automatically restarts the SSH service upon configuration changes.
- **Security Enhancements:** Enforces secure defaults such as disabled root login and public key authentication.

## 📚 Other Resources
- https://www.google.com/search?client=firefox-b-d&q=sshd+why+to+deactivate+pam
- https://man7.org/linux/man-pages/man5/sshd_config.5.html

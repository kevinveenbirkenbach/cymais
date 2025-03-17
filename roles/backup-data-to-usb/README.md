# Automated USB Backup

## Description

This Ansible role automates data backups to a swappable USB device. It triggers the backup process automatically when the USB is mounted, allowing for customizable source and destination paths and integrating with systemd for reliable execution.

## Overview

Optimized for Archlinux, this role ensures that backups are performed consistently with minimal manual intervention. It leverages efficient synchronization methods and provides a seamless integration with systemd to manage the backup service.

## Purpose

The primary purpose of this role is to simplify the backup process for systems that rely on removable USB devices. It is designed to reduce the risk of data loss by automating backups, ensuring that data is safely and consistently synchronized whenever the device is connected.

## Features

- **Automatic Trigger:** Initiates the backup process immediately upon USB mount.
- **Customizable Paths:** Easily configure the source directory and backup destination.
- **Systemd Integration:** Manages the backup process via a dedicated systemd service.
- **Efficient Synchronization:** Utilizes rsync with incremental backup strategies for optimal performance.
- **Optimized for Archlinux:** Tailored for Archlinux systems using the rolling release model.

## Credits 📝

Developed and maintained by **Kevin Veen-Birkenbach**. Special thanks to [OpenAI ChatGPT](https://chat.openai.com/share/a75ca771-d8a4-4b75-9912-c515ba371ae4) for its assistance in developing this role.
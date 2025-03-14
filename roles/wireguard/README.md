# Wireguard

## Description

This role manages [Wireguard](https://www.wireguard.com/) on the host. It installs the necessary Wireguard packages, configures sysctl settings for IPv4/IPv6 forwarding, and deploys the Wireguard configuration file to enable the VPN service using [wg-quick](https://www.wireguard.com/quickstart/).

## 📌 Overview

Optimized for both [Arch Linux](https://wiki.archlinux.org/index.php/WireGuard) and [Ubuntu/Debian](https://wireguard.com/install/), this role performs the following tasks:
- Installs Wireguard tools using the appropriate package manager.
- Copies a sysctl configuration file to enable IP forwarding and proper IPv6 settings.
- Deploys a host-specific Wireguard configuration file to `/etc/wireguard/wg0.cymais.conf`.
- Uses systemd handlers to restart the Wireguard service and reload sysctl settings.

## Purpose

The primary purpose of this role is to set up and manage a Wireguard VPN configuration on the host. By automating package installation and configuration file deployment, it ensures that the VPN service is enabled with optimal network settings for secure connectivity.

## Features

- **Multi-Platform Support:** Installs Wireguard tools using [pacman](https://wiki.archlinux.org/title/Pacman) on Arch Linux and [apt](https://en.wikipedia.org/wiki/APT_(software)) on Ubuntu/Debian.
- **Sysctl Configuration:** Deploys a sysctl configuration file to manage IPv4/IPv6 forwarding and related network parameters.
- **Wireguard Configuration:** Copies a host-specific Wireguard configuration file to `/etc/wireguard/wg0.cymais.conf`.
- **Service Management:** Provides handlers to restart the Wireguard service and reload sysctl settings.

## Administration
For detailed client setup instructions, please see the [Administration](./Administration.md) file.

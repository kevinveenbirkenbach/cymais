# Postfix

## Description

This role installs and configures [Postfix](https://en.wikipedia.org/wiki/Postfix_(software)) – a mail transfer agent – on the target system. It deploys a preconfigured aliases file (using a Jinja2 template) that defines mail redirections and standard aliases for local mail delivery.

## 📌 Overview

Optimized for secure and reliable mail delivery, this role:
- Installs Postfix via [pacman](https://wiki.archlinux.org/title/Pacman).
- Provides a default aliases file to route system mail appropriately.
- Configures essential Postfix parameters via a templated main configuration file (if needed).

## Purpose

The primary purpose of this role is to set up a robust mail transfer agent configuration for local mail delivery. It ensures that system-generated mail (such as error messages) is delivered to the correct administrative address.

## Features

- **Postfix Installation:** Ensures the [Postfix](https://en.wikipedia.org/wiki/Postfix_(software)) package is installed.
- **Aliases Configuration:** Deploys a default aliases file to direct system mail.
- **System Integration:** Works in conjunction with the administrator user role for secure mail routing.

# systemd-notifier Ansible Role

Author: Kevin Veen-Birkenbach (kevin@veen.world)

## Description

This Ansible role installs a systemd service that sends notifications via both `systemd-notifier-telegram` and `systemd-notifier-email` when any service fails.

Features include:

- Configuration of a systemd service for notification.
- Dependency management for the `systemd-notifier-telegram` and `systemd-notifier-email` roles.

This role was created as part of a conversation with OpenAI's ChatGPT and can be found [here](https://chat.openai.com/share/96e4ca12-0888-41c0-9cfc-29c0180f0dba).

## Role Dependencies

This role has the following dependencies:

- `systemd-notifier-telegram`
- `systemd-notifier-email`

## Features

- Installs a systemd service for sending notifications.
- Integrates with both Telegram and Email for notification delivery.

## Contact Information

For any questions or feedback, please contact the author:

Author: Kevin Veen-Birkenbach
Email: kevin@veen.world
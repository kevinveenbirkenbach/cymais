# systemd_notifier Ansible Role

Author: Kevin Veen-Birkenbach (kevin@veen.world)

## Description

This Ansible role installs a systemd service that sends notifications via both `systemd_notifier_telegram` and `systemd_notifier_email` when any service fails.

Features include:

- Configuration of a systemd service for notification.
- Dependency management for the `systemd_notifier_telegram` and `systemd_notifier_email` roles.

This role was created as part of a conversation with OpenAI's ChatGPT and can be found [here](https://chat.openai.com/share/96e4ca12-0888-41c0-9cfc-29c0180f0dba).

## License

This Ansible role is licensed under the AGPL v3 License. See the LICENSE file for the full license text.

## Role Dependencies

This role has the following dependencies:

- `systemd_notifier_telegram`
- `systemd_notifier_email`

## Features

- Installs a systemd service for sending notifications.
- Integrates with both Telegram and Email for notification delivery.

## Contact Information

For any questions or feedback, please contact the author:

Author: Kevin Veen-Birkenbach
Email: kevin@veen.world
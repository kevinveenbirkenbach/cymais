## Description

This Ansible role installs the necessary components for sending Telegram notifications through systemd when any service fails. It configures the `systemd-notifier-telegram` service and handles the setup of Telegram bot parameters and notification templates.

Features include:

- Installation and configuration of a Telegram notifier service.
- Customizable templates for Telegram messages sent on service failure.

This role is part of the `systemd-notifier` suite, which provides a comprehensive solution for service failure notifications in a systemd environment.

## Requirements

This role has the following requirements:

- Access to a Telegram bot token for sending messages.
- Availability of the `curl` package on the target system.

## Role Variables

The following variables can be customized in the role's `vars/main.yml` file:

- `systemd_telegram_folder`: The path to the folder where Telegram-related scripts and configurations will be stored.
- `systemd_telegram_script`: The full path to the systemd-telegram.sh script.

This role was created as part of a conversation with OpenAI's ChatGPT and can be found [here](https://chat.openai.com/share/96e4ca12-0888-41c0-9cfc-29c0180f0dba).

## Usage

To use this role, include it as a dependency in your playbook or role that requires Telegram notifications. Ensure that the `systemd-notifier-telegram` role is correctly referenced and configured.

## Contact Information

For any questions or feedback, please contact the author:

Author: Kevin Veen-Birkenbach
Email: kevin@veen.world
# Automated Telegram Alerts for Service Failures

## Description

This role installs and configures the necessary components for sending notifications via systemd when a service fails. It sets up the `systemd-notifier-telegram` service and configures parameters and customizable templates for sending messages through [Telegram](https://telegram.org).

## Overview

Optimized for real-time alerts, this role is a key component of the overall [`systemd-notifier` suite](../). It ensures that, upon failure of a critical service, a Telegram message is automatically sent to notify administrators and enable prompt troubleshooting.

## Purpose

The primary purpose of this role is to provide a robust solution for automated Telegram notifications in a systemd environment. By integrating with Telegram’s Bot API and using customizable message templates, it delivers clear and timely alerts about service failures, thereby enhancing system observability and reliability.

## Features

- **Service Installation & Configuration:** Installs and configures necessary components (including the `curl` package).
- **Customizable Templates:** Supports tailored Telegram message templates for service failure notifications.
- **Secure Notifications:** Leverages systemd to trigger alerts automatically when services fail.
- **Suite Integration:** Part of the [`systemd-notifier` suite](../) which includes related roles such as [systemd-notifier-email](../systemd-notifier-email/README.md) and others.
  
## Further Information

This role was developed as part of a conversation with OpenAI's ChatGPT and can be found [here](https://chat.openai.com/share/96e4ca12-0888-41c0-9cfc-29c0180f0dba).

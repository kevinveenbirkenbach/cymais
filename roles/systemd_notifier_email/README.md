# systemd_notifier_email Ansible Role

Author: Kevin Veen-Birkenbach (kevin@veen.world)

## Description

This Ansible role installs the necessary components for sending email notifications through systemd when any service fails. It configures the `systemd_notifier_email` service and handles the setup of email parameters and templates.

Features include:

- Installation and configuration of an email sending service.
- Customizable email templates for service failure notifications.

This role is part of the `systemd_notifier` suite, which provides a comprehensive solution for service failure notifications in a systemd environment.

This role was created as part of a conversation with OpenAI's ChatGPT and can be found [here](https://chat.openai.com/share/96e4ca12-0888-41c0-9cfc-29c0180f0dba).

## Requirements

This role has the following requirements:

- Access to an SMTP server for sending email notifications.
- Availability of the `msmtp` package on the target system.

## Role Variables

The following variables can be customized in the role's `vars/main.yml` file:

- `systemd_notifier_email_folder`: The path to the folder where email-related scripts and configurations will be stored.

## Usage

To use this role, include it as a dependency in your playbook or role that requires email notifications. Ensure that the `systemd_notifier_email` role is correctly referenced and configured.

## License

This Ansible role is licensed under the AGPL v3 License. See the LICENSE file for the full license text.

## Contact Information

For any questions or feedback, please contact the author:

Author: Kevin Veen-Birkenbach
Email: kevin@veen.world
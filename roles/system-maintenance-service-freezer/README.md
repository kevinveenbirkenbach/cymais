# System Maintenance Service Freezer

## Overview
This Ansible role is designed to manage system services through freezing (disabling) and defrosting (enabling) actions. It automates the process of managing crucial system services, especially useful for maintenance tasks like backups, cleanups, and updates.

## Monitoring
To monitor the sucess of the script and the status of systemctl timers execute:

```bash
watch -n 2 systemctl list-timers
```

## Role Variables
- `system_maintenance_services`: List of services to be managed by this role.

## Usage
Configure the role by defining the required variables. The role creates systemd service files that control the specified services based on the `freeze` or `defrost` actions.

For further details and usage examples, refer to the chat conversation with ChatGPT: [Link to ChatGPT Conversation](https://chat.openai.com/share/212af169-1b57-41df-bd2d-c3d32eb1331b).

## Dependencies
- `systemd-notifier`: Ensure this role is present for handling service failures.

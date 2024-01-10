# Health Check for Docker Volumes

## Description

This role checks for anonymous Docker volumes that are not bound to a container and may be left over from previous operations. It provides a cleanup mechanism by identifying such volumes, excluding any that are whitelisted, and possibly taking action against them.

## Files

- `vars/main.yml`: Variable definitions for the script's directory and whitelist.
- `handlers/main.yml`: Handlers to reload and restart the systemd service and timer.
- `files/health-docker-volumes.sh`: The script that checks for anonymous Docker volumes and excludes whitelisted volumes.
- `tasks/main.yml`: Tasks to create necessary directories, copy scripts, and create systemd service and timer.
- `templates/health-docker-volumes.cymais.service.j2`: Systemd service template, including the whitelisted volumes as a parameter.
- `templates/health-docker-volumes.timer.j2`: Systemd timer template.
- `meta/main.yml`: Meta information declaring dependencies for the role.

## Usage

Include this role in your playbook and set the `path_administrator_scripts` variable to determine where the health check scripts should reside. Define `whitelisted_anonymous_volumes` in `vars/main.yml` with an array of volume IDs that should be ignored by the health check.

Ensure that the `systemd-notifier` dependency is satisfied for error notifications.

## Created with AI
This script was created with the help of AI. The full conversation you find [here](https://chat.openai.com/share/1fa829f1-f001-4111-b1d4-1b2e3d583da2).


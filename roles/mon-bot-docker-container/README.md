# Health Check for Docker Containers

## Description

This Ansible role is designed to ensure the health of Docker containers running on a system. It includes a script that checks for unhealthy or exited Docker containers and sets up a systemd service and timer to regularly execute this check.

## Files

- `vars/main.yml`: Variable definitions for the script's directory.
- `handlers/main.yml`: Handlers to reload and restart the systemd service and timer.
- `files/mon-bot-docker-container.sh`: The script that checks the container health.
- `tasks/main.yml`: Tasks to create necessary directories, copy scripts, and create systemd service and timer.
- `templates/mon-bot-docker-container.cymais.service.j2`: Systemd service template.
- `templates/mon-bot-docker-container.cymais.timer.j2`: Systemd timer template.
- `meta/main.yml`: Meta information declaring dependencies for the role.

## Usage

To use this role, include it in your playbook and set the `path_administrator_scripts` variable to the desired path for the health check scripts.

Ensure that the `alert-compose` dependency is satisfied for error notifications.
# Docker Auto Restart

This role was implemented to address the classic issue: ["Have you tried turning it off and on again?"](https://www.youtube.com/watch?v=rksCTVFtjM4). The problem initially arose with the `fetchmail` container in [Mailu](../roles/docker/mailu), which fails if only some containers, and not the full docker-compose composition, are restarted.

## Overview

This role automates the restart process for all `docker-compose` instances within a specified directory. It ensures consistent restarts of services while avoiding issues caused by partial restarts.

## Features
- Automatically detects and restarts `docker-compose` instances in the given directory.
- Uses a Python script to perform service restarts with `docker-compose restart`.
- Integrates with `systemd` for scheduled or manual execution.
- Designed for idempotency and ease of integration.

## Requirements
- `docker-compose` must be installed on the target system.
- Python 3.x is required to execute the provided script.
- This role depends on the `system-maintenance-lock` role for handling system-wide locking during restarts.

## Installation
1. Clone or include this role in your Ansible project.
2. Define the required variables in your playbook or inventory:
   ```yaml
   path_administrator_scripts: "/path/to/administrator/scripts/"
   restart_docker_volumes_folder: "/path/to/restart/volumes/"
   on_calendar_restart_dockers: "daily"
   ```

## Usage
Include this role in your playbook:
```yaml
- hosts: all
  roles:
    - docker-auto-restart
```

The role will:
1. Set up the necessary directories and scripts.
2. Configure a `systemd` service to restart docker-compose instances.
3. Optionally schedule restarts via a systemd timer.

## Acknowledgments
This role was developed with the assistance of [ChatGPT](https://openai.com/chatgpt), including insights and optimizations from this [conversation](https://chatgpt.com/share/674c6870-fcc4-800f-a19e-b20621b24317). Special thanks for providing guidance on error handling, Ansible best practices, and Python integration.

---

Feel free to contribute or provide feedback via the [repository issues page](https://github.com/kevinveenbirkenbach/cymais/issues).
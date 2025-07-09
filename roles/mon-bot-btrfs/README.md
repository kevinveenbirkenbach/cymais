# mon-bot-btrfs

## Description
Checks the health of all mounted Btrfs filesystems by inspecting device error counters.

## Features
- Iterates over every Btrfs filesystem.
- Runs `btrfs device stats` and alerts if any error counters are non-zero.
- Hooks into systemd and a timer for regular checks.
- On failure, calls `alert-compose.cymais@…` for notification.

## Usage
Just include this role in your playbook; it will:
1. Deploy a small shell script under `{{ path_administrator_scripts }}/mon-bot-btrfs/`.
2. Install a `.service` and `.timer` unit.
3. Send alerts via `alert-compose` if any filesystem shows errors.

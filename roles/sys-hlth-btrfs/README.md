# sys-hlth-btrfs

## Description
Checks the health of all mounted Btrfs filesystems by inspecting device error counters.

## Features
- Iterates over every Btrfs filesystem.
- Runs `btrfs device stats` and alerts if any error counters are non-zero.
- Hooks into systemd and a timer for regular checks.
- On failure, calls `sys-alm-compose.infinito@…` for notification.

## Usage
Just include this role in your playbook; it will:
1. Deploy a small shell script under `{{ path_administrator_scripts }}/sys-hlth-btrfs/`.
2. Install a `.service` and `.timer` unit.
3. Send alerts via `sys-alm-compose` if any filesystem shows errors.

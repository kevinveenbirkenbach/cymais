# Administration Notes

## Delete all containers, networks and volumes

```bash
docker compose down -v
```

## Show the state of all containers

```bash
watch -n 2 "docker compose ps -a"
```

## Health Logs

```bash
docker inspect --format='{{json .State.Health}}' <container_id>
```

### 🔍 Logging with `journalctl`

All Docker Compose actions triggered by this role are logged to the system journal using `systemd-cat`. Output is simultaneously shown in the terminal and available via `journalctl`.

To view logs for a specific application:

```bash
journalctl -t docker-compose-<application_id> -f
```

Replace `<application_id>` with the actual project name (e.g. `discourse`, `nextcloud`, etc.).

This enables persistent and searchable logs for all container setups and rebuilds.



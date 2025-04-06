# Docker Compose

## Delete all containers, networks and volumes

```bash
docker compose down -v
```

## Show the state of all containers

```bash
watch -n 2 "docker compose ps -a"
```
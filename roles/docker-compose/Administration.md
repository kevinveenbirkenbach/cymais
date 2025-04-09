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
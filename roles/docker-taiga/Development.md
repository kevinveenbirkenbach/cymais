# Development 

## Build front container

```bash
docker compose up -d --force-recreate taiga-front
```

## Debug

Verify front configuration:

```bash
docker compose exec -it taiga-front cat /usr/share/nginx/html/conf.json
```
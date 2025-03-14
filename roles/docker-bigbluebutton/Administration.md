## Administration

## cleanup
```bash
    docker compose down -v
```

## check container status 
```bash
watch -n 2 "docker compose ps -a"
```

## database access
```bash
 sudo docker-compose exec -it postgres psql -U postgres
```
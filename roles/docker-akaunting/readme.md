# docker akaunting
## clean up
### delete all containers
```bash
export COMPOSE_HTTP_TIMEOUT=600
export DOCKER_CLIENT_TIMEOUT=600
cd /home/administrator/docker-compose/akaunting/ && docker-compose down
```
### delete all volumes
```bash
docker volume rm akaunting_akaunting-data akaunting_akaunting-db akaunting_akaunting-modules
```

## setup
```bash
cd /home/administrator/docker-compose/akaunting/
export COMPOSE_HTTP_TIMEOUT=600
export DOCKER_CLIENT_TIMEOUT=600
AKAUNTING_SETUP=true docker-compose -p akaunting up -d
docker-compose down
docker-compose -p akaunting up -d
```

## rebuild
```bash
cd /home/administrator/docker-compose/akaunting/
export COMPOSE_HTTP_TIMEOUT=600
export DOCKER_CLIENT_TIMEOUT=600
docker-compose down
docker network prune
docker-compose -p akaunting up -d --force-recreate
```


## Further information
- https://github.com/akaunting/docker

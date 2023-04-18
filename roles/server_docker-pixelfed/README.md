# role server_docker-pixelfed

## hard cleanup
```bash
server_docker-compose down
docker volume rm pixelfed_application_data pixelfed_database pixelfed_redis_data
```

## update
```bash 
cd /home/administrator/server_docker-compose/pixelfed/ &&
server_docker-compose down &&
docker network prune -f &&
server_docker-compose pull &&
server_docker-compose build &&
server_docker-compose -p pixelfed up -d --force-recreate
```

## inspect 

```bash
server_docker-compose ps -a
server_docker-compose logs -f
```

## further information
- https://hub.docker.com/r/zknt/pixelfed
- https://blog.pixelfed.de/2020/05/29/pixelfed-in-docker/
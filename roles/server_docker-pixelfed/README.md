# role server_docker-pixelfed

## Go into application container
```bash
sudo docker-compose exec -it application bash
```

## hard cleanup
```bash
docker-compose down
docker volume rm pixelfed_application_data pixelfed_database pixelfed_redis_data
```

## update
```bash 
cd {{path_docker_compose_files}}pixelfed/ &&
docker-compose down &&
docker network prune -f &&
docker-compose pull &&
docker-compose build &&
docker-compose -p pixelfed up -d --force-recreate
```

## inspect 

```bash
docker-compose ps -a
docker-compose logs -f
```

## further information
- https://hub.docker.com/r/zknt/pixelfed
- https://blog.pixelfed.de/2020/05/29/pixelfed-in-docker/
# role docker-pixelfed

## hard cleanup
```bash
docker-compose down
docker volume rm pixelfed_application_data pixelfed_database pixelfed_redis_data
```

## update
```bash 
cd /home/administrator/docker-compose/pixelfed/
docker-compose down
docker-compose pull
docker-compose up -d
```

## inspect 

```bash
docker-compose logs
```

## further information
- https://hub.docker.com/r/zknt/pixelfed
- https://blog.pixelfed.de/2020/05/29/pixelfed-in-docker/
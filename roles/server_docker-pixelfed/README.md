# role server_docker-pixelfed

## access application
```bash
docker-compose exec -it application bash
```

## access database
```bash
docker-compose exec -it database mariadb -u pixelfed -p
```

## cleanup instagram imports
### mysql
```bash
DELETE from import_posts WHERE 1;
DELETE from import_jobs WHERE 1;
DELETE from import_datas WHERE 1;
DELETE from statuses where created_at < "2022-12-01 22:15:39";
DELETE from media where deleted_at >= "2023-07-28 14:39:05";
```
### files
```bash
docker-compose exec -u "www-data" application rm -rv "/var/www/storage/app/imports/1"
docker-compose exec -u "www-data" application php artisan schedule:run
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
# role docker-gitea

## update
```bash 
cd {{docker_compose.directories.instance}}
docker-compose down
docker-compose pull
docker-compose up -d
```
Keep in mind to track and to don't interrupt the update process until the migration is done. 

## set variables
```bash
  COMPOSE_HTTP_TIMEOUT=600
  DOCKER_CLIENT_TIMEOUT=600
```

## recreate
```bash
cd {{docker_compose.directories.instance}} && docker-compose -p gitea up -d --force-recreate
```

## database access
To access the database execute
```bash
  docker-compose exec -it database /bin/mysql -u gitea -p
```
## bash in application
docker-compose exec -it application /bin/sh
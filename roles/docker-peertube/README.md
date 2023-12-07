# docker peertube

## track docker container status
```bash
watch -n 2 "docker ps  -a | grep peertube"
```

## clean rebuild
```bash
cd {{docker_compose_instances_directory}}peertube/ &&
docker-compose down 
docker volume rm peertube_assets peertube_config peertube_data peertube_database peertube_redis
docker-compose up -d 
```

## access terminal
```bash
docker-compose exec -it application /bin/bash
```

## update config
```bash
apt update && apt install nano && nano ./config/default.yaml
```

## get root pasword
```bash
docker logs peertube-application-1 | grep -A1 root
```

## further information
- https://docs.joinpeertube.org/install-docker
- https://github.com/Chocobozzz/PeerTube/issues/3091
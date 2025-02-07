# docker peertube

## track docker container status
```bash
watch -n 2 "docker ps  -a | grep peertube"
```

## clean rebuild
```bash
cd {{path_docker_compose_instances}}peertube/ &&
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

## upgrade version
- https://docs.joinpeertube.org/install/docker

## further information
- https://docs.joinpeertube.org/install-docker
- https://github.com/Chocobozzz/PeerTube/issues/3091
- [OIDC Plugin installation](https://chatgpt.com/c/67a4f448-4be8-800f-8639-4c15cb2fb44e)
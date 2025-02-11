# role docker

## maintenance

### list unused volumes
```bash 
    docker volume ls -q -f "dangling=true"
```

### remove all unused volumes
```bash 
    docker volume rm $(docker volume ls -q -f "dangling=true")
```

### network issues
```bash 
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network prune -f
sudo iptables -t nat -F DOCKER
sudo iptables -t nat -F DOCKER-USER
```


## performance
- https://forums.docker.com/t/mysql-slow-performance-in-docker/37179/21

## see
- https://stackoverflow.com/questions/37599128/docker-how-do-you-disable-auto-restart-on-a-container

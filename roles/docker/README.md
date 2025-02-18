# Docker Role 🚀

This role is part of the [CyMaIS Project](https://github.com/kevinveenbirkenbach/cymais), maintained and developed by [Kevin Veen-Birkenbach](https://www.veen.world/).

---

## Maintenance 🛠️

### List Unused Volumes
```bash
docker volume ls -q -f "dangling=true"
```

### Remove All Unused Volumes
```bash
docker volume rm $(docker volume ls -q -f "dangling=true")
```

### Network Issues Fixes
```bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network prune -f
sudo iptables -t nat -F DOCKER
sudo iptables -t nat -F DOCKER-USER
```

---

## Warning ⚠️

**Caution:** The following instructions will delete **all Docker containers and volumes** on your server.  
Make sure you have backups or that you're certain you want to clean your Docker environment completely.

---

## Cleaning Up Docker Containers and Volumes 🧹

### Delete All Docker Containers
```bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

### Delete All Docker Volumes
```bash
docker volume rm $(docker volume ls -q)
```

---

Enjoy using this role and happy containerizing! 🎉
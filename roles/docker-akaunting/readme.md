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
```

Check Webinterface and then execute: 

```bash
docker-compose down
docker-compose -p akaunting up -d
```
## enter akaunting container

docker exec -it akaunting bash

curl https://getcomposer.org/download/2.4.1/composer.phar --output composer.phar

## manuel update
```bash
php /var/www/html/artisan update:all
php /var/www/html/artisan update:db
```

## composer
curl http://some.url --output

php composer.phar install


## recover

### recover all volumes
Keep in mind to set the $akaunting_db_password!

```bash
cd /usr/local/bin/docker-volume-backup &&
machine_id="$(sha256sum /etc/machine-id)" &&
bash docker-volume-recover.sh akaunting_akaunting-modules ${machine_id:0:64} &&
bash docker-volume-recover.sh akaunting_akaunting-data ${machine_id:0:64} &&
bash docker-volume-recover.sh akaunting_akaunting-db ${machine_id:0:64} akaunting-db "$akaunting_db_password" akaunting
```

docker exec -it akaunting-db /bin/mysql -u admin --password=$akaunting_db_password akaunting

### rebuild containers
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
- https://akaunting.com/forum/discussion/installation-update/updating-to-300-failed-cant-manually-update-either
- https://akaunting.com/forum/discussion/installation-update/not-able-to-update-core
- https://akaunting.com/forum/discussion/installation-update/update-to-203-not-able-to-finalize-core-installation
# docker akaunting

## new setup
```bash
cd {{path_docker_compose_files}}akaunting/
export COMPOSE_HTTP_TIMEOUT=600
export DOCKER_CLIENT_TIMEOUT=600
AKAUNTING_SETUP=true docker-compose -p akaunting up -d
```

Check Webinterface and then execute: 

```bash
docker-compose down
docker-compose -p akaunting up -d
```

## administration

### get logs

```bash
docker exec -it akaunting tail -n 300 storage/logs/laravel.log 
```

### enter akaunting container

```bash
docker exec -it akaunting bash
```

### enter database container

```bash
docker exec -it akaunting-db /bin/mysql -u admin --password=$akaunting_db_password akaunting
```

## manuel update
```bash
php artisan about
php artisan cache:clear
php artisan view:clear
php artisan migrate:status
php artisan update:all
php artisan update:db
```

## composer
```bash
curl https://getcomposer.org/download/2.4.1/composer.phar --output composer.phar
```

```bash
php composer.phar install
```

## full backup routine

```bash
# DO SET MANUEL VARIABLES >>
export akaunting_db_password=XXXXXXXXX
export backup_version=XXXXXXXXX
# << DO SET MANUEL VARIABLES

# set automatic variables
export machine_id="$(sha256sum /etc/machine-id)"
export COMPOSE_HTTP_TIMEOUT=600
export DOCKER_CLIENT_TIMEOUT=600

# destroy all containers
cd {{path_docker_compose_files}}akaunting/ && 
docker-compose down &&
docker network prune -f

# delete all volumes
docker volume rm akaunting_akaunting-data akaunting_akaunting-db akaunting_akaunting-modules

# rebuild containers
docker-compose pull &&
docker-compose build &&
docker-compose -p akaunting up -d --force-recreate

# recover all volumes
cd {{path_administrator_scripts}}backup-docker-to-local &&
bash recover-docker-from-local.sh akaunting_akaunting-modules ${machine_id:0:64} "$backup_version" &&
bash recover-docker-from-local.sh akaunting_akaunting-data ${machine_id:0:64} "$backup_version" &&
bash recover-docker-from-local.sh akaunting_akaunting-db ${machine_id:0:64} "$backup_version" akaunting-db "$akaunting_db_password" akaunting

```

## todo 
- implement build when new akaunting version is set

## Further information
- https://github.com/akaunting/docker
- https://akaunting.com/forum/discussion/installation-update/updating-to-300-failed-cant-manually-update-either
- https://akaunting.com/forum/discussion/installation-update/not-able-to-update-core
- https://akaunting.com/forum/discussion/installation-update/update-to-203-not-able-to-finalize-core-installation
- https://akaunting.com/forum/discussion/installation-update/how-to-perform-manual-update-v2116
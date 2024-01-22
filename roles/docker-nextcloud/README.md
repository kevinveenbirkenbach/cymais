# role docker-nextcloud

## modify config
Enter container:
```bash
  docker-compose exec -it application /bin/sh
```

Afterwards modify config:
```bash
apk add --no-cache nano && nano config/config.php
```

## update

To update the nextcloud container execute the following commands on the server:
```bash
  docker-compose exec -it -u www-data application /var/www/html/occ maintenance:mode --on &&
  export COMPOSE_HTTP_TIMEOUT=600 &&
  export DOCKER_CLIENT_TIMEOUT=600 &&
  docker-compose down
```

Afterwards update the ***nextcloud_version*** variable to the next version and run the this repository with this ansible role.

It is only possible to update from one to the next major version at a time

Wait for the update to finish.

You can verify that the update is finished by checking the following logs:

```bash
docker-compose logs application
```

and

```bash
docker-compose exec -it application top
```

If nextcloud stays in the maintenance mode after the update try the following:

```bash
  docker-compose exec -it -u www-data application /var/www/html/occ maintenance:mode --on
  docker-compose exec -it -u www-data application /var/www/html/occ upgrade
  docker-compose exec -it -u www-data application /var/www/html/occ maintenance:mode --off
```

If the update process fails execute

```bash
  docker-compose exec -it -u www-data application /var/www/html/occ maintenance:repair
```

and disable the not functioning apps.

## recover latest backup
```bash
cd {{path_docker_compose_instances}}nextcloud &&
docker-compose down &&
docker-compose exec -i database mysql -u nextcloud -pPASSWORT nextcloud < "/Backups/$(sha256sum /etc/machine-id | head -c 64)/backup-docker-to-local/latest/nextcloud_database/sql/backup.sql" &&
cd {{path_administrator_scripts}}backup-docker-to-local &&
bash ./recover-docker-from-local.sh "nextcloud_data" "$(sha256sum /etc/machine-id | head -c 64)"
```

## database
### database access
To access the database execute
```bash
  docker-compose exec -it database mysql -u nextcloud -D nextcloud -p
```

### recreate database with new volume:
```bash
docker-compose run --detach --name database --env MYSQL_USER="nextcloud" --env MYSQL_PASSWORD=PASSWORD --env MYSQL_ROOT_PASSWORD=PASSWORD --env MYSQL_DATABASE="nextcloud" -v nextcloud_database:/var/lib/mysql
```

The process can be checked with:

```bash
show processlist;
```

## occ

To use occ run:

```bash
  docker-compose exec -it -u www-data application /var/www/html/occ
```

## app relevant tables
- oc_appconfig
- oc_migrations

### initialize duplicates

```bash
  docker-compose exec -it -u www-data application /var/www/html/occ duplicates:find-all --output
```

### unlock files
```bash
  docker-compose exec -it -u www-data application /var/www/html/occ maintenance:mode --on
  docker-compose exec -it nextcloud_database_1 mysql -u nextcloud -pPASSWORD1234132 -D nextcloud -e "delete from oc_file_locks where 1"
  docker-compose exec -it -u www-data application /var/www/html/occ maintenance:mode --off
```

## architecture
### Maria DB
Until NC24 MariaDB version has to be used.

## performance
### 504 Gateway Timeout

```bash
  docker-compose logs web --tail 1000 | grep 504
```

#### See
- https://support.f5.com/csp/article/K48373902
- https://github.com/nextcloud/server/issues/25436
- https://help.nextcloud.com/t/update-to-next-cloud-21-0-2-has-get-an-error/117028/23?page=2
- https://serverfault.com/questions/178671/nginx-php-fpm-504-gateway-time-out-error-with-almost-zero-load-on-a-test-se
- https://help.nextcloud.com/t/solved-manual-lemp-install-php-fpm-timing-out/39070

## further information
- https://github.com/nextcloud/docker/blob/master/.examples/docker-compose/with-nginx-proxy/mariadb/fpm/docker-compose.yml
- https://goneuland.de/nextcloud-upgrade-auf-neue-versionen-mittels-docker/
- https://help.nextcloud.com/t/cant-start-nextcloud-because-the-version-of-the-data-is-higher-than-the-docker-image-version-and-downgrading-is-not-supported/109438
- https://github.com/nextcloud/docker/issues/1302
- https://help.nextcloud.com/t/update-to-22-failed-with-database-error-updated/120682
- https://help.nextcloud.com/t/nc-update-to-21-0-0-beta1-exception-database-error/101124/4
- https://wolfgang.gassler.org/reset-password-mariadb-mysql-docker/
- https://unix.stackexchange.com/questions/478855/ansible-docker/container/and-depends-on
- https://github.com/gdiepen/docker-convenience-scripts
- https://help.nextcloud.com/t/several-issues-after-upgrading-to-nextcloud-21/113118/3
- https://forum.openmediavault.org/index.php?thread/31782-docker-nextcloud-talk-plugin-and-turnserver/
- https://help.nextcloud.com/t/nextcloud-talk-im-docker/container/turn-server-auf-docker-host-kein-video/84133/10

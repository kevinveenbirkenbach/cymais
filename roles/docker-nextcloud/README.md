# role docker-nextcloud

## database access
To access the database execute
```bash
  docker exec -it nextcloud_database_1 /bin/mysql -u nextcloud -p
```

## update

To update the nextcloud container execute the following commands on the server:

```bash
export COMPOSE_HTTP_TIMEOUT=600
export DOCKER_CLIENT_TIMEOUT=600
cd /home/administrator/docker-compose/nextcloud &&
docker-compose pull &&
docker-compose up -d
```

Afterwards update the ***nextcloud_version*** variable to the next version and run the server manager.

It is only possible to update from one to the next major version at a time

You can check the status of the update by typing in:

```bash
  docker logs nextcloud_application_1
```

If nextcloud stays in the maintenance mode after the update try the following:

```bash
  docker exec -it -u www-data nextcloud_application_1 /var/www/html/occ maintenance:mode --on
  docker exec -it -u www-data nextcloud_application_1 /var/www/html/occ upgrade
  docker exec -it -u www-data nextcloud_application_1 /var/www/html/occ maintenance:mode --off
```

If the update process fails execute

```bash
  docker exec -it -u www-data nextcloud_application_1 /var/www/html/occ maintenance:repair
```

and disable the mal functioning apps.

## recover latest backup
```bash
cd /home/administrator/docker-compose/nextcloud &&
docker-compose down &&
cd /usr/local/bin/docker-volume-backup &&
bash ./docker-volume-recover.sh "nextcloud_data" "$(sha256sum /etc/machine-id | head -c 64)" &&
bash ./docker-volume-recover.sh "nextcloud_database" "$(sha256sum /etc/machine-id | head -c 64)"
```

## database debuging

```bash
  docker exec -it -u www-data nextcloud_database_1 /bin/mysql -u nextcloud -p
```
## occ

To use occ run:

```bash
  docker exec -it -u www-data nextcloud_application_1 /var/www/html/occ
```

## unlock files
```bash
  docker exec -it -u www-data nextcloud_application_1 /var/www/html/occ maintenance:mode --on
  docker exec -it nextcloud_database_1 mysql -u nextcloud -pPASSWORD1234132 -D nextcloud -e "delete from oc_file_locks where 1"
  docker exec -it -u www-data nextcloud_application_1 /var/www/html/occ maintenance:mode --off
```

## further information
- https://github.com/nextcloud/docker/blob/master/.examples/docker-compose/with-nginx-proxy/mariadb/fpm/docker-compose.yml
- https://goneuland.de/nextcloud-upgrade-auf-neue-versionen-mittels-docker/
- https://help.nextcloud.com/t/cant-start-nextcloud-because-the-version-of-the-data-is-higher-than-the-docker-image-version-and-downgrading-is-not-supported/109438
- https://github.com/nextcloud/docker/issues/1302
- https://help.nextcloud.com/t/update-to-22-failed-with-database-error-updated/120682
- https://help.nextcloud.com/t/nc-update-to-21-0-0-beta1-exception-database-error/101124/4
- https://wolfgang.gassler.org/reset-password-mariadb-mysql-docker/
- https://unix.stackexchange.com/questions/478855/ansible-docker-container-and-depends-on
- https://github.com/gdiepen/docker-convenience-scripts
- https://techoverflow.net/2021/08/17/how-to-fix-nextcloud-4047-innodb-refuses-to-write-tables-with-row_formatcompressed-or-key_block_size/

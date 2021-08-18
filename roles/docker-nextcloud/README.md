# role docker-nextcloud

## database access
To access the database execute
```bash
  docker exec -it nextcloud_database_1 /bin/mysql -u nextcloud -p
```

## update

To update the nextcloud container execute the following commands on the server:

```bash
  # Requiered:
  docker stop nextcloud_application_1 && docker rm $(docker ps -aqf "name=nextcloud_application_1") &&
  # Optional:
  docker stop nextcloud_web_1 && docker rm $(docker ps -aqf "name=nextcloud_web_1") &&
  docker stop nextcloud_database_1 && docker rm $(docker ps -aqf "name=nextcloud_database_1") &&
  docker stop nextcloud_cron_1 && docker rm $(docker ps -aqf "name=nextcloud_cron_1") &&
  docker stop nextcloud_redis_1 && docker rm $(docker ps -aqf "name=nextcloud_redis_1")
```
Afterwards update the ***nextcloud_version*** variable to the next version and run the server manager.

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

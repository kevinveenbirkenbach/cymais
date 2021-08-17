# role docker-nextcloud

## database access
To access the database execute
```bash
  docker exec -it nextcloud_database_1 /bin/mysql -u nextcloud -p
```

## update

To update the nextcloud container execute the following commands on the server:

```bash
  docker pull nextcloud
  docker stop nextcloud_application_1
  docker rm <your_nextcloud_container>
```
Afterwards run the server manager.

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
- https://goneuland.de/nextcloud-upgrade-auf-neue-versionen-mittels-docker/
- https://help.nextcloud.com/t/cant-start-nextcloud-because-the-version-of-the-data-is-higher-than-the-docker-image-version-and-downgrading-is-not-supported/109438

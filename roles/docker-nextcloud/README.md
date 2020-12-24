# role docker-nextcloud

## database access
To access the database execute
```bash
  docker exec -it nextcloud_database_1 /bin/mysql -u nextcloud -p
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

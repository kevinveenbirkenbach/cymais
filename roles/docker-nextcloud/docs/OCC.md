
# OCC (Nextcloud Command Line) 🔧

Reference for frequently used OCC commands, including user and app management.

## General Use

To use OCC, run:
```bash
docker-compose exec -it -u www-data application /var/www/html/occ
```

## App Administration
```bash
docker compose exec -u www-data application php occ config:list {{app_name}}
```

## Initialize Duplicates
```bash
docker-compose exec -it -u www-data application /var/www/html/occ duplicates:find-all --output
```

## Unlock Files
```bash
docker-compose exec -it -u www-data application /var/www/html/occ maintenance:mode --on
docker-compose exec -it nextcloud_database_1 mysql -u nextcloud -pPASSWORD1234132 -D nextcloud -e "delete from oc_file_locks where 1"
docker-compose exec -it -u www-data application /var/www/html/occ maintenance:mode --off
```
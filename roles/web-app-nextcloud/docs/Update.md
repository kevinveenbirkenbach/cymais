# Update 🔄

To update the Nextcloud container, execute the following commands on the server:
```bash
docker exec -it -u www-data nextcloud-application /var/www/html/occ maintenance:mode --on &&
export COMPOSE_HTTP_TIMEOUT=600 &&
export DOCKER_CLIENT_TIMEOUT=600 &&
docker-compose down
```

Afterwards, update the ***applications.nextcloud.version*** variable to the next version and run this repository with this Ansible role.

> **Note:**  
> It is only possible to update from one to the next major version at a time.  
> Wait for the update to finish.

Verify the update by checking the logs:
```bash
docker-compose logs application
```
and
```bash
docker-compose exec -it application top
```

If Nextcloud remains in maintenance mode after the update, try the following:
```bash
docker exec -it -u www-data nextcloud-application/var/www/html/occ maintenance:mode --on
docker exec -it -u www-data nextcloud-application /var/www/html/occ upgrade
docker exec -it -u www-data nextcloud-application /var/www/html/occ maintenance:mode --off
```

If the update process fails, execute:
```bash
docker exec -it -u www-data nextcloud-application /var/www/html/occ maintenance:repair --include-expensive
```
and disable any non-functioning apps.

---

## Recover Latest Backup 💾

```bash
cd {{path_docker_compose_instances}}nextcloud &&
docker-compose down &&
docker-compose exec -i database mysql -u nextcloud -pPASSWORT nextcloud < "/Backups/$(sha256sum /etc/machine-id | head -c 64)/backup-docker-to-local/latest/nextcloud_database/sql/backup.sql" &&
cd {{path_administrator_scripts}}backup-docker-to-local &&
bash ./recover-web-app-from-local.sh "nextcloud_data" "$(sha256sum /etc/machine-id | head -c 64)"
```

## Other Resources

- [Nextcloud Upgrade via Docker by Goneuland](https://goneuland.de/nextcloud-upgrade-auf-neue-versionen-mittels-docker/)
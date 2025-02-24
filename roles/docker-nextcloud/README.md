# Docker Nextcloud Role 🚀

This repository contains an Ansible role for deploying and managing [Nextcloud](https://nextcloud.com/) using [Docker](https://www.docker.com/). It covers configuration modifications, updates, backups, database management, and more. Additionally, OIDC (OpenID Connect) is supported (for example, via **Keycloak**).

---

## Modify Config 🔧

### Enter the Container
```bash
docker-compose exec -it application /bin/sh
```

### Modify the Configuration
Inside the container, install a text editor and edit the config:
```bash
apk add --no-cache nano && nano config/config.php
```

---

## Update 🔄

To update the Nextcloud container, execute the following commands on the server:
```bash
docker-compose exec -it -u www-data application /var/www/html/occ maintenance:mode --on &&
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
docker-compose exec -it -u www-data application /var/www/html/occ maintenance:mode --on
docker-compose exec -it -u www-data application /var/www/html/occ upgrade
docker-compose exec -it -u www-data application /var/www/html/occ maintenance:mode --off
```

If the update process fails, execute:
```bash
docker-compose exec -it -u www-data application /var/www/html/occ maintenance:repair --include-expensive
```
and disable any non-functioning apps.

---

## Recover Latest Backup 💾

```bash
cd {{path_docker_compose_instances}}nextcloud &&
docker-compose down &&
docker-compose exec -i database mysql -u nextcloud -pPASSWORT nextcloud < "/Backups/$(sha256sum /etc/machine-id | head -c 64)/backup-docker-to-local/latest/nextcloud_database/sql/backup.sql" &&
cd {{path_administrator_scripts}}backup-docker-to-local &&
bash ./recover-docker-from-local.sh "nextcloud_data" "$(sha256sum /etc/machine-id | head -c 64)"
```

---

## Database Management 🗄️

### Database Access
To access the database, execute:
```bash
docker-compose exec -it database mysql -u nextcloud -D nextcloud -p
```

### Recreate Database with New Volume
```bash
docker-compose run --detach --name database --env MYSQL_USER="nextcloud" --env MYSQL_PASSWORD=PASSWORD --env MYSQL_ROOT_PASSWORD=PASSWORD --env MYSQL_DATABASE="nextcloud" -v nextcloud_database:/var/lib/mysql
```

---

## OCC (Nextcloud Command Line) 🔧

To use OCC, run:
```bash
docker-compose exec -it -u www-data application /var/www/html/occ
```

### Make user admin via cli
```bash
docker compose exec -it -u www-data application php occ group:adduser admin {{username}}
```

### Delete user via CLI
```bash
docker compose exec -it -u www-data application php occ user:delete {{username}}
```
---



## App Relevant Tables 🗃️

- `oc_appconfig`
- `oc_migrations`

### Initialize Duplicates
```bash
docker-compose exec -it -u www-data application /var/www/html/occ duplicates:find-all --output
```

### Unlock Files
```bash
docker-compose exec -it -u www-data application /var/www/html/occ maintenance:mode --on
docker-compose exec -it nextcloud_database_1 mysql -u nextcloud -pPASSWORD1234132 -D nextcloud -e "delete from oc_file_locks where 1"
docker-compose exec -it -u www-data application /var/www/html/occ maintenance:mode --off
```

---

# Identity and Access Management (IAM)

## OpenID Connect (OIDC) Support 🔐

OIDC is supported in this role—for example, via **Keycloak**. OIDC-specific tasks are included when enabled, allowing integration of external authentication providers seamlessly.

### Verify OIDC Configuration

```bash
docker compose exec -u www-data application /var/www/html/occ config:app:get sociallogin custom_providers
```

## LDAP 

More information: https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/user_auth_ldap.html

## Federation

If users are just created via Keycloak and not via LDAP, they have a different username. Due to this reaso concider to use LDAP to guaranty that the username is valid. 

---

## Further Information ℹ️

- [Nextcloud Docker Example with Nginx Proxy, MariaDB, and FPM](https://github.com/nextcloud/docker/blob/master/.examples/docker-compose/with-nginx-proxy/mariadb/fpm/docker-compose.yml)
- [Nextcloud Upgrade via Docker by Goneuland](https://goneuland.de/nextcloud-upgrade-auf-neue-versionen-mittels-docker/)
- [Nextcloud Data Version Issue](https://help.nextcloud.com/t/cant-start-nextcloud-because-the-version-of-the-data-is-higher-than-the-docker-image-version-and-downgrading-is-not-supported/109438)
- [Nextcloud Docker Issue #1302](https://github.com/nextcloud/docker/issues/1302)
- [Update to Nextcloud 22 Failed Database Error](https://help.nextcloud.com/t/update-to-22-failed-with-database-error-updated/120682)
- [Nextcloud 21.0.0-beta1 Database Error](https://help.nextcloud.com/t/nc-update-to-21-0-0-beta1-exception-database-error/101124/4)
- [Reset Password for MariaDB/MySQL in Docker](https://wolfgang.gassler.org/reset-password-mariadb-mysql-docker/)
- [Ansible Docker Container and depends_on Issue](https://unix.stackexchange.com/questions/478855/ansible-docker/container/and-depends-on)
- [Docker Convenience Scripts by gdiepen](https://github.com/gdiepen/docker-convenience-scripts)
- [Issues After Upgrading to Nextcloud 21](https://help.nextcloud.com/t/several-issues-after-upgrading-to-nextcloud-21/113118/3)
- [Nextcloud Talk Plugin and Turnserver in Docker](https://forum.openmediavault.org/index.php?thread/31782-docker-nextcloud-talk-plugin-and-turnserver/)
- [Nextcloud Talk on Docker: Turn Server Issues](https://help.nextcloud.com/t/nextcloud-talk-im-docker/container/turn-server-auf-docker-host-kein-video/84133/10)

---
## Author

**Developed by:** Kevin Veen-Birkenbach  
**Website:** [https://www.veen.world/](https://www.veen.world/)

*This README.md was created with the help of [ChatGPT](https://chatgpt.com/share/67a5312c-7248-800f-ae27-0288c1c82f1d).*

---
*Enjoy and happy containerizing! 😄*



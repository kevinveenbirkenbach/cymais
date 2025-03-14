# Administration 

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
### User Administration 

#### List Users
```bash
docker compose exec -it -u www-data application php occ user:list
```

#### Sync Users
```bash
docker compose exec -it -u www-data application php occ user:sync
```

#### Create user via CLI
```bash
docker compose exec -it -u www-data application php occ user:add {{username}}
```

#### Make user admin via cli
```bash
docker compose exec -it -u www-data application php occ group:adduser admin {{username}}
```

#### Delete user via CLI
```bash
docker compose exec -it -u www-data application php occ user:delete {{username}}
```
---

### App Administration
```bash
docker compose exec -u www-data application php occ config:list {{app_name}}
```

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

## Apps

### App Relevant Tables 🗃️

- `oc_appconfig`
- `oc_migrations`

### Cospend 

#### Relevant SQL Commands for Cospend
Debugguging Migrations: 

https://github.com/julien-nc/cospend-nc/issues/325
```sql
-- Show all Cospend Tables
SHOW TABLES where Tables_in_nextcloud LIKE "%cospend%";
-- Show Cospend Configuration
SELECT * FROM `oc_appconfig` WHERE appid LIKE "%cospend%";
-- Show Cospend Database Migrations 
SELECT * FROM `oc_migrations` WHERE app LIKE "%cospend%";
```

# Identity and Access Management (IAM)

## OpenID Connect (OIDC) Support 🔐

OIDC is supported in this role—for example, via **Keycloak**. OIDC-specific tasks are included when enabled, allowing integration of external authentication providers seamlessly.

### Verify OIDC Configuration

```bash
docker compose exec -u www-data application /var/www/html/occ config:app:get sociallogin custom_providers
```

## LDAP 

More information: https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/user_auth_ldap.html

## Get all relevant entries except password

```sql
SELECT * FROM `oc_appconfig` WHERE appid LIKE "%ldap%" and configkey != "s01ldap_agent_password";
```

## Update User with LDAP values

```bash
docker compose exec -it -u www-data application php occ ldap:check-user --update {{username}}
```

## Federation

If users are just created via Keycloak and not via LDAP, they have a different username. Due to this reaso concider to use LDAP to guaranty that the username is valid. 

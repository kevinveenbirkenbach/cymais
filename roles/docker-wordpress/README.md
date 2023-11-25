# role docker-wordpress

## database 

## access database
To access the database execute
```bash
  docker-compose exec -it database /bin/mysql -u wordpress -p
```

## upgrade database
To upgrade the database execute
```bash
  docker-compose exec -it database /bin/mysql_upgrade --user=root --password=
```

## change database root password
- https://wolfgang.gassler.org/reset-password-mariadb-mysql-docker/
- https://www.digitalocean.com/community/tutorials/how-to-reset-your-mysql-or-mariadb-root-password

## bash in application
docker-compose exec -it wordpress-application-1 /bin/sh

## update wp-config.php
```bash
apt update && apt install nano && nano wp-config.php
```

## multiside
- https://multilingualpress.de/doku/wordpress-multisite-installieren-einrichten/
- https://pressable.com/knowledgebase/adding-or-changing-the-domain-on-a-wordpress-multisite/
- https://wpengine.com/support/how-to-change-a-multi-site-primary-domain/

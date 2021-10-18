# role docker-wordpress

## database access
To access the database execute
```bash
  docker exec -it wordpress_database_1 /bin/mysql -u wordpress -p
```
## bash in application
docker exec -it wordpress_application_1 /bin/sh

## update wp-config.php
```bash
cat > wp-config.php << EOF
<?php
#content
EOF
```

## multiside
- https://multilingualpress.de/doku/wordpress-multisite-installieren-einrichten/

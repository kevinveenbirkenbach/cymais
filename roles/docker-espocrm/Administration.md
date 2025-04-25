# Administration

## 🗑️ Cleanup (Remove instance & volumes)
```bash
cd {{path_docker_compose_instances}}espocrm/
docker compose down
# EspoCRM keeps all uploaded files in the *data* volume
docker volume rm espocrm_data espocrm_database
cd {{path_docker_compose_instances}} && rm -vR {{path_docker_compose_instances}}espocrm
```

## 🔍 Access EspoCRM container shell
```bash
docker compose exec -it web /bin/bash
```

## 🛠️ Database migrations (after image upgrade)
EspoCRM applies migrations automatically on start‑up. To run them manually:
```bash
docker compose exec -it web php command.php upgrade
```

## 🗄️ Backup database
```bash
# Dump the MySQL/MariaDB database
docker exec espocrm_database /usr/bin/mysqldump -u root -p$MYSQL_ROOT_PASSWORD espocrm > backup_$(date +%F).sql
```

## 🧹 Clear cache
```bash
docker compose exec web php command.php clear cache
```
# Friendica Docker Role

This role manages the setup, reset, and maintenance of a Friendica instance running with Docker.

## Overview 🚀

Friendica is a decentralized social networking platform. This role helps manage Friendica in a containerized environment with Docker and provides tools for debugging, resetting, and maintaining the installation.

## Prerequisites 🛠️

Ensure you have the following:
- Docker and Docker Compose installed
- A central MariaDB instance running
- Necessary permissions to manage Docker and database configurations

## Usage 📚

### Full Reset 🚫➡️✅

The following environment variables need to be defined for successful operation:

- `DB_ROOT_PASSWORD`: The root password for the MariaDB instance

To completely reset Friendica, including its database and volumes, run:
```bash
docker exec -i central-mariadb mariadb -u root -p"${DB_ROOT_PASSWORD}" -e "DROP DATABASE IF EXISTS friendica; CREATE DATABASE friendica;"
docker compose down
rm -rv /mnt/hdd/data/docker/volumes/friendica_data
docker volume rm friendica_data
```

### Reset Database 🗄️

#### Manual Method:
1. Connect to the MariaDB instance:
   ```bash
   docker exec -it central-mariadb mariadb -u root -p
   ```
2. Run the following commands:
   ```sql
   DROP DATABASE friendica;
   CREATE DATABASE friendica;
   exit;
   ```

#### Automatic Method:
```bash
DB_ROOT_PASSWORD="your_root_password"
docker exec -i central-mariadb mariadb -u root -p"${DB_ROOT_PASSWORD}" -e "DROP DATABASE IF EXISTS friendica; CREATE DATABASE friendica;"
```

### Enter the Application Container 🔍

To access the application container:
```bash
docker compose exec -it application sh
```

### Debugging Tools 🛠️

#### Check Environment Variables
```bash
docker compose exec -it application printenv
```

#### Inspect Volume Data
```bash
ls -la /var/lib/docker/volumes/friendica_data/_data/
```

### Autoinstall 🌟

Run the following command to autoinstall Friendica:
```bash
docker compose exec --user www-data -it application bin/console autoinstall
```

### Reinitialization 🔄

#### Docker Only:
```bash
docker-compose up -d --force-recreate
```

#### Full Reinitialization:
```bash
docker-compose up -d --force-recreate && sleep 2; docker compose exec --user www-data -it application bin/console autoinstall;
```

### Configuration Information ℹ️

#### General Configuration:
```bash
cat /var/lib/docker/volumes/friendica_data/_data/config/local.config.php
```

#### Email Configuration:
```bash
docker compose exec -it application cat /etc/msmtprc
```

### Email Debugging ✉️

To send a test email:
```bash
docker compose exec -it application msmtp --account=system_email -t test@test.de
```

## Additional Resources 📖

- [Friendica Docker Hub](https://hub.docker.com/_/friendica)
- [Friendica Installation Docs](https://wiki.friendi.ca/docs/install)
- [Friendica GitHub Repository](https://github.com/friendica/docker)
- [Open Issue: Login Mask does not change with OIDC activated](https://github.com/friendica/friendica/issues/14743)

---

📜 Created by [Kevin Veen-Birkenbach](https://www.veen.world/)


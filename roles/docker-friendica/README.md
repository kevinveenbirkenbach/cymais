# role friendica

## Delete all
docker exec -i central-mariadb mariadb -u root -p"${DB_ROOT_PASSWORD}" -e "DROP DATABASE IF EXISTS friendica; CREATE DATABASE friendica;"; docker compose down; rm -rv /mnt/hdd/data/docker/volumes/friendica_data; docker volume rm friendica_data

## Reset Database
### Manual
DROP DATABASE friendica;
CREATE DATABASE friendica;
exit;

### Automatic
DB_ROOT_PASSWORD="your_root_password"
docker exec -i central-mariadb mariadb -u root -p"${DB_ROOT_PASSWORD}" -e "DROP DATABASE IF EXISTS friendica; CREATE DATABASE friendica;"

## Enter application 

docker compose exec -it application sh


## debugging

## Check environment variables
docker compose exec -it application printenv

ls -la /var/lib/docker/volumes/friendica_data/_data/

## autoinstall
docker compose exec --user www-data -it application bin/console autoinstall

## reinitialisation

### docker
docker-compose up -d --force-recreate

### full
docker-compose up -d --force-recreate && sleep 2; docker compose exec --user www-data -it application bin/console autoinstall; 

### info
```bash 
## Check general config
cat /var/lib/docker/volumes/friendica_data/_data/config/local.config.php
## Check environment variables
docker compose exec -it application printenv
## Check email configuration
docker compose exec -it application cat /etc/msmtprc
```

## email debugging:
docker compose exec -it application msmtp --account=system_email -t kevin@veen.world

## create user
INSERT INTO user (guid, username, email, password, verified, register_date, account_expires_on, account_expired)
VALUES (
    UUID(), -- Generiert eine eindeutige Benutzer-ID
    'newusername', -- Benutzername
    'newuser@example.com', -- E-Mail-Adresse
    MD5('newpassword'), -- Passwort (kann durch Bcrypt ersetzt werden, siehe unten)
    1, -- Verifizierungsstatus (1 = verifiziert)
    NOW(), -- Registrierungsdatum
    '0001-01-01 00:00:00', -- Kontodauer unbegrenzt
    0 -- Konto ist nicht abgelaufen
);



## More information
- https://hub.docker.com/_/friendica
- https://wiki.friendi.ca/docs/install
- https://github.com/friendica/docker
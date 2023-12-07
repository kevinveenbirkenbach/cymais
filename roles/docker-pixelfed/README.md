# Pixelfed Docker Server Role

This README details the steps to manage your Pixelfed instance running in a Docker container. This setup is part of the docker-pixelfed role within Kevin Veen-Birkenbach's cymais located at [this GitHub repository](https://github.com/kevinveenbirkenbach/cymais/tree/master/roles/docker-pixelfed). 

## Accessing Services

### Application Access
To gain shell access to the application container, run the following command:
```bash
docker-compose exec -it application bash
```

### Database Access
To access the MariaDB instance in the database container, run the following command:
```bash
docker-compose exec -it database mariadb -u pixelfed -p
```

## Instagram Import Cleanup

If you have imported posts from Instagram, you can clean up the imported data and files as follows:

### Database Cleanup
Run these commands inside your MariaDB shell to remove import related data:
```bash
DELETE from import_posts WHERE 1;
DELETE from import_jobs WHERE 1;
DELETE from import_datas WHERE 1;
DELETE from statuses where created_at < "2022-12-01 22:15:39";
DELETE from media where deleted_at >= "2023-07-28 14:39:05";
```

### File System Cleanup
Run these commands to remove the imported files and trigger the cleanup job:
```bash
docker-compose exec -u "www-data" application rm -rv "/var/www/storage/app/imports/1"
docker-compose exec -u "www-data" application php artisan schedule:run
```

## Full Cleanup (Reset)

For a hard reset, which will delete all data and stop all services, use the following commands:
```bash
docker-compose down
docker volume rm pixelfed_application_data pixelfed_database pixelfed_redis_data
```

## Update Procedure

To update your Pixelfed instance, navigate to the directory where your `docker-compose.yml` file is located and run these commands:
```bash 
cd {{docker_compose_instances_directory}}pixelfed/ &&
docker-compose down &&
docker network prune -f &&
docker-compose pull &&
docker-compose build &&
docker-compose -p pixelfed up -d --force-recreate
```

## Inspecting the Services

To see the status of all services or follow the logs, use these commands:
```bash
docker-compose ps -a
docker-compose logs -f
```

## Debug
To debug the system set APP_DEBUG to true, like descriped [here](https://docs.pixelfed.org/technical-documentation/config/).

```bash
nano config/app.php
php artisan cache:clear
php artisan route:cache
php artisan view:clear
php artisan config:cache
```

## Modifying files
```bash
apt update && apt upgrade && apt install nano
```

## Further Reading
For additional information, refer to these resources:
- [Docker image on Docker Hub](https://hub.docker.com/r/zknt/pixelfed)
- [Blog Post about running Pixelfed in Docker](https://blog.pixelfed.de/2020/05/29/pixelfed-in-docker/)

Author: Kevin Veen-Birkenbach, [https://www.veen.world](https://www.veen.world), [kevin@veen.world](mailto:kevin@veen.world)

This README was optimized with the help of OpenAI's ChatGPT. You can view the conversation [here](https://chat.openai.com/share/3daea33f-2e30-46e9-a709-a9c93e823ed9).
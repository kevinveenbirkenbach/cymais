# Docker Akaunting Setup Guide

## !!!DANGER!!!

**AKAUNTING CONTAINS VERY MUCH PROPERITARY COMPONENTS. IT IS ALMOST IMPOSSIBLE TO USE THIS SOFTWARE FOR FREE IN A PRODUCTIVE ENVIRONMENT. UPDATES MAY BREAK YOUR INSTALLATION. IN THE PAST UPDATES LEADED TO THE REDUCTION OF FREE FEATURES AND INSTEAD THEY BECOME PAYD FEATURES. THIS LEADED TO THAT USERS COULD NOT MAINTAINE THERE COMPANIES IN AKAUNTING ANYMORE**

I recommend to use instead [Open Project](../docker-openproject/) and/or [GNUCash](../pc-gnucash/).

This role still exist in case, that you want to setup Akaunting and you're willing to pay, but I recommend to don't use akaunting.  

## Introduction
This guide details the process of setting up Akaunting, a free and online accounting software, using Docker. It's tailored to help you deploy and manage an Akaunting instance efficiently using Docker and Docker Compose.

## Prerequisites
- Docker and Docker Compose installed.
- Basic understanding of Docker concepts.
- Access to the command line or terminal.

## Installation Steps

@ATTENTION Variable ```#AKAUNTING_SETUP: true``` needs to be set

### New Manual Setup
1. **Navigate to Docker Compose Directory**: Change to the directory containing your Docker Compose files for Akaunting.

    ```bash
    cd {{path_docker_compose_instances}}akaunting/
    ```

2. **Set Environment Variables**: These are necessary to prevent timeouts during long operations.

    ```bash
    export COMPOSE_HTTP_TIMEOUT=600
    export DOCKER_CLIENT_TIMEOUT=600
    ```

3. **Start Akaunting Service**: This command will initialize the Akaunting setup.

    ```bash
    AKAUNTING_SETUP=true docker-compose -p akaunting up -d
    ```

4. **Check Web Interface**: Ensure the web interface is operational.

5. **Restart Services**: To finalize the setup, restart the services.

    ```bash
    docker-compose down
    docker-compose -p akaunting up -d
    ```

### Administration
- **View Logs**: To check the latest logs of Akaunting.

    ```bash
    docker-compose exec -it akaunting tail -n 300 storage/logs/laravel.log 
    ```

- **Access Containers**: For troubleshooting or configuration.
  - Akaunting Container: `docker-compose exec -it akaunting bash`
  - Database Container: `docker-compose exec -it akaunting-db /bin/mariadb -u admin --password=$akaunting_db_password akaunting`

### Manual Update
Execute PHP artisan commands in the following order for updating Akaunting:

```bash
php artisan about
php artisan cache:clear
php artisan view:clear
php artisan migrate:status
php artisan update:all
php artisan update:db
```

### Composer
To install Composer, a PHP dependency management tool:

```bash
curl https://getcomposer.org/download/2.4.1/composer.phar --output composer.phar
php composer.phar install
```

### Full Backup Routine
Detailed steps for backing up your Akaunting instance, including setting manual and automatic variables, destroying containers, removing volumes, and rebuilding and recovering volumes. (Refer to the full backup routine script in the original README).

### Setting Variables
Variables are crucial in configuring your Akaunting setup. Ensure you set the following variables correctly in your environment:

- `docker_compose_instance_directory`: Set this variable to the path where your Docker Compose files for Akaunting are located.
- `akaunting_db_password`, `applications.akaunting.version`, `applications.akaunting.company_name`, `applications.akaunting.company_email`, `applications.akaunting.setup_admin_email`, and `akaunting_setup_admin_password`: These should be set in your `.env` files as per your requirements.

### Additional Configuration
- **SSL Certificate**: The guide includes steps to receive a certificate for your domain.
- **Nginx Configuration**: Necessary steps to configure Nginx as a reverse proxy for Akaunting.
- **Database and Runtime Environment**: Instructions on how to set up the `db.env` and `run.env` files for database and runtime configurations.

## Further Information
For more details, visit the [Akaunting Docker Repository](https://github.com/akaunting/docker) and the [Akaunting Forums](https://akaunting.com/forum).

## Contribution and Feedback

Your contributions and feedback are welcome. Please reach out for support or queries at kevin@veen.world.

## Author

This script is developed by Kevin Veen-Birkenbach. You can reach out to him at kevin@veen.world or visit his website at https://www.veen.world.
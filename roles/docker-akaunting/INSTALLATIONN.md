# Installation Steps

@ATTENTION Variable ```#AKAUNTING_SETUP: true``` needs to be set

## New Manual Setup
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
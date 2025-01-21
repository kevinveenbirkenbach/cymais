#!/bin/sh

# Check if the necessary parameters are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <domain> <docker_compose_instance_directory>"
    exit 1
fi

# Assign parameters
domain="$1"
docker_compose_instance_directory="$2"

# Copy certificates
cp "/etc/letsencrypt/live/$domain/privkey.pem" "$docker_compose_instance_directory/certs/key.pem" || exit 1
cp "/etc/letsencrypt/live/$domain/fullchain.pem" $docker_compose_instance_directory/certs/cert.pem || exit 1

# Reload Nginx in all containers within the Docker Compose setup
cd "$docker_compose_instance_directory" || exit 1
docker compose ps --services | while read -r service; do
    docker compose exec "$service" nginx -s reload && exit 0
done

# Restart all docker containers if no nginx reload is possible
docker compose restart || exit 1
# docker mastodon

## create configuration
```bash
    docker-compose run --rm web bundle exec rake mastodon:setup
```

## Setup with existing configuration
```bash 
docker-compose run --rm web bundle exec rails db:migrate
```

## cleanup
```bash
cd {{path_docker_compose_instances}}mastodon/
docker-compose down
docker volume rm mastodon_data mastodon_database mastodon_redis
cd {{path_docker_compose_instances}} &&
rm -vR {{path_docker_compose_instances}}mastodon
```

## access terminal
```bash
docker-compose exec -it web /bin/bash
```

## set rights

After setting up mastodon you need to give the rights 

```bash
docker-compose exec -it -u root web chown -R 991:991 public
```

### Running Database Migrations

To ensure all required database tables and structures are in place after an update, you can run database migrations directly within the Mastodon web container. Use the following command:

```bash
docker compose exec -it web bash -c "RAILS_ENV=production bin/rails db:migrate"
```

This command enters the web container and runs migrations in production mode, updating the database structure to match the current version of the Mastodon software. If your Mastodon web container is named differently in your `docker-compose.yml`, replace `web` with the appropriate container name.

## further information
- https://goneuland.de/mastodon-mit-docker-und-traefik-installieren/
- https://gist.github.com/TrillCyborg/84939cd4013ace9960031b803a0590c4
- https://www.2daygeek.com/linux-command-check-website-is-up-down-alive/
- https://vitobotta.com/2022/11/07/setting-up-a-personal-mastodon-instance/
- https://www.digitalocean.com/community/tutorials/how-to-scale-your-mastodon-server


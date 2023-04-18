# docker mastodon
## create configuration
```bash
    server_docker-compose run --rm web bundle exec rake mastodon:setup
```
## cleanup
```bash
cd /home/administrator/server_docker-compose/mastodon/
server_docker-compose down
docker volume rm mastodon_data mastodon_database mastodon_redis
cd /home/administrator/server_docker-compose/ &&
rm -vR /home/administrator/server_docker-compose/mastodon
```

## access terminal
```bash
docker exec -it mastodon-web-1 /bin/bash
```

## set rights

After setting up mastodon you need to give the rights 

```bash
docker exec -it -u root mastodon-web-1 chown -R 991:991 public
```

## further information
- https://goneuland.de/mastodon-mit-server_docker-und-traefik-installieren/
- https://gist.github.com/TrillCyborg/84939cd4013ace9960031b803a0590c4
- https://www.2daygeek.com/linux-command-check-website-is-up-down-alive/
- https://vitobotta.com/2022/11/07/setting-up-a-personal-mastodon-instance/
# docker bigbluebutton
@TODO Database needs to be decoupled 

Role to deploy [BigBlueButton](https://bigbluebutton.org/). 

## maintanace

### cleanup
```bash
    docker compose down -v
```

### check container status 
```bash
watch -n 2 "docker compose ps -a"
```

### database access
```bash
 sudo docker-compose exec -it postgres psql -U postgres
```

## SSO
- https://docs.bigbluebutton.org/greenlight/v3/external-authentication/

## further information
- https://github.com/bigbluebutton/docker
- https://docs.bigbluebutton.org/greenlight/gl-install.html#setting-bigbluebutton-credentials
- https://goneuland.de/big-blue-button-mit-docker-und-traefik-installieren/
- https://github.com/docker/compose/issues/4799
- https://www.cyberciti.biz/faq/linux-command-to-remove-virtual-interfaces-or-network-aliases/
- https://www.cyberciti.biz/faq/linux-restart-network-interface/
- https://stackoverflow.com/questions/53347951/docker-network-not-found
- https://github.com/bigbluebutton/docker/issues/325
- https://mattdyson.org/blog/2024/11/self-hosting-bluesky-pds/

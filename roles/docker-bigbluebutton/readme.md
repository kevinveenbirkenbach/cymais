# docker bigbluebutton
Role to deploy [BigBlueButton](https://bigbluebutton.org/). 

## naintance

### cleanup
```bash
    docker-compose down;
    docker volume rm bigbluebutton_bigbluebutton bigbluebutton_html5-static bigbluebutton_vol-freeswitch bigbluebutton_vol-kurento bigbluebutton_vol-mediasoup bigbluebutton_database
```

### check container status 
```bash
watch -n 2 "docker ps -a | grep bigbluebutton"
```

## Further information
- https://github.com/bigbluebutton/docker
- https://docs.bigbluebutton.org/greenlight/gl-install.html#setting-bigbluebutton-credentials
- https://goneuland.de/big-blue-button-mit-docker-und-traefik-installieren/
- https://github.com/docker/compose/issues/4799
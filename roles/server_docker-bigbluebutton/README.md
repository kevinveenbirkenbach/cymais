# docker bigbluebutton
Role to deploy [BigBlueButton](https://bigbluebutton.org/). 

## maintanace

### cleanup
```bash
    docker-compose down;
    docker volume rm bigbluebutton_bigbluebutton bigbluebutton_html5-static bigbluebutton_vol-freeswitch bigbluebutton_vol-kurento bigbluebutton_vol-mediasoup bigbluebutton_database
```

### check container status 
```bash
watch -n 2 "docker ps -a | grep bigbluebutton"
```

## further information
- https://github.com/bigbluebutton/docker
- https://docs.bigbluebutton.org/greenlight/gl-install.html#setting-bigbluebutton-credentials
- https://goneuland.de/big-blue-button-mit-server_docker-und-traefik-installieren/
- https://github.com/docker/compose/issues/4799
- https://www.cyberciti.biz/faq/linux-command-to-remove-virtual-interfaces-or-network-aliases/
- https://www.cyberciti.biz/faq/linux-restart-network-interface/
- https://stackoverflow.com/questions/53347951/server_docker-network-not-found
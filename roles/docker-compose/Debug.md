    # Debug

    ## Bind for 127.0.0.1:XXXX failed: port is already allocated

    If their are port allocated messages ``Bind for 127.0.0.1:XXXX failed: port is already allocated"`` execute the following command:

    ```bash
    find /opt/docker -maxdepth 1 -type d -exec bash -c '[ -f "{}/docker-compose.yml" ] && echo "Stopping: {}" && docker compose -f "{}/docker-compose.yml" down' \; &
    systemctl restart docker
    find /opt/docker -maxdepth 1 -type d -exec bash -c '[ -f "{}/docker-compose.yml" ] && echo "Starting: {}" && docker compose -f "{}/docker-compose.yml" up -d' \; &
    ```

    Then try to run the ansible script again.


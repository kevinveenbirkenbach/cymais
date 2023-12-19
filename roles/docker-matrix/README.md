# Docker-Matrix Role README

## Overview

This document serves as the README for the `docker-matrix` role, a part of the `CyMaIS` project. This role automates the deployment of a Matrix server using Docker. 

Matrix is an open-source project that provides a protocol for secure, decentralized, real-time communication. It offers features like end-to-end encrypted chat, VoIP, and file sharing, catering to both individual and enterprise users. With a focus on interoperability, Matrix can bridge with other communication systems, offering a unified platform for messaging and collaboration.

## Dependencies

- `nginx-docker-reverse-proxy` (see `meta/main.yml`)

## Files and Their Functions

1. **`vars/main.yml`**: Defines variables such as `docker_compose_instance_directory`.
2. **`handlers/main.yml`**: Contains handlers like `recreate matrix` for restarting the Matrix service.
3. **`tasks/main.yml`**: Contains main tasks like creating directories and configuration files.
4. **`templates/log.config.j2`**: Template for the Matrix server's logging configuration.
5. **`templates/homeserver.yaml.j2`**: Template for the main configuration file of the Matrix server.
6. **`templates/docker-compose.yml.j2`**: Docker-Compose template for setting up the Matrix server and database.

## Important Administration Commands

- **Create Matrix Users**: 
  ```
  docker compose exec -it synapse register_new_matrix_user -u [Username] -p [Password] -a -c /data/homeserver.yaml http://localhost:8008
  ```
- **Execute Docker-Compose Commands**:
  - Restart services: 
    ```
    docker-compose up -d --force-recreate
    ```
  - View logs:
    ```
    docker-compose logs
    ```
## Sources

### Guides

- https://cyberhost.uk/element-matrix-setup/
- https://www.linode.com/docs/guides/how-to-install-the-element-chat-app/
- https://hub.docker.com/r/vectorim/element-web

## Links to ChatGPT Conversations

- https://chat.openai.com/share/d4485223-3750-4b0b-9733-45776c55d7cf
- https://chat.openai.com/share/f68873d9-aae9-4a1e-83b6-c3f23705a4ad
- https://chat.openai.com/share/11690964-9997-4e44-b63f-3c384a5ddc1d
- https://chat.openai.com/share/6f537c30-7337-47ed-8c85-19306e0eb74b
- https://chat.openai.com/share/31974492-2950-4dbc-8a83-edd7e1569bec
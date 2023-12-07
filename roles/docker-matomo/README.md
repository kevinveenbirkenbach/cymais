# Docker Matomo Role

This Ansible role deploys a Matomo analytics platform instance using Docker.

## Requirements

- Docker and Docker-Compose installed on the host machine.
- Nginx installed for reverse proxy configuration.
- Certbot installed for SSL certificate generation.

## Role Variables

- `domain`: The domain where Matomo will be accessible.
- `administrator_email`: The email used for SSL certificate registration.
- `path_docker_compose_instances`: Path to store Docker Compose files.
- `http_port`: The host port that Matomo will be accessible on.
- `matomo_database_password`: Password for the Matomo database.

## Dependencies

- `nginx-docker-reverse-proxy`: An Ansible role for configuring the reverse proxy.

## Example Playbook

```yaml
- hosts: servers
  roles:
    - { role: docker-matomo, domain: 'example.com', http_port: 8080 }
```

## AI Generated
This script was created with the help of ChatGPT. The full conversation is [here](https://chat.openai.com/share/49e0c7e4-a2af-4a04-adad-7a735bdd85c4) available.
# docker-keycloak

## Description 🌟

This role automates the setup and configuration of Keycloak in a Docker environment. 
Keycloak is an open-source identity and access management solution. 
The role integrates Keycloak with PostgreSQL as a database and supports operation behind a reverse proxy like NGINX.

## Features ✨
- Set up Keycloak as a Docker container.
- Use PostgreSQL as the database.
- Customizable configuration of Keycloak environment variables.
- Support for running behind a reverse proxy (e.g., NGINX).
- Automatic creation and management of Docker Compose files.

## Requirements 📋
- Docker and Docker Compose must be installed on the target system.
- A working NGINX proxy for forwarding requests to Keycloak (optional).

## Variables ⚙️

### Main Variables

Defined in `vars/main.yml`:

| Variable                        | Description                                                      |
|---------------------------------|------------------------------------------------------------------|
| `application_id`   | Name of the Docker Compose project. Default: `keycloak`.         |
| `database_type`                 | Type of the database. Default: `postgres`.                      |
| `database_password`             | Password for the PostgreSQL database user.                      |

### Additional Variables (Templates)

| Variable                        | Description                                                      |
|---------------------------------|------------------------------------------------------------------|
| `keycloak_version`              | Version of the Keycloak image.                                  |
| `domain`                        | Domain where Keycloak will be accessible.                       |
| `keycloak_administrator_username` | Admin username for Keycloak.                                   |
| `keycloak_administrator_password` | Admin password for Keycloak.                                   |
| `database_host`                 | Host of the PostgreSQL database.                                |
| `database_name`                 | Name of the PostgreSQL database.                                |
| `database_username`             | Username for the PostgreSQL database.                          |
| `http_port`                     | Port where Keycloak will be accessible (default: `8080`).       |
| `docker_restart_policy`         | Docker restart policy (e.g., `always`, `unless-stopped`).       |

## Tasks 🛠️

The role performs the following main tasks:

1. **Include database and proxy configuration files:**
   - Integration of a PostgreSQL database.
   - Setup of a reverse proxy for the domain.

2. **Generate `docker-compose.yml`:**
   - Automatically generate the Docker Compose file based on templates and variables.

3. **Start Docker containers:**
   - The role launches the Keycloak project using Docker Compose.

## Example: Usage 🚀

Here is an example of how to use this role in a playbook:

```yaml
- name: Setup Keycloak with Docker
  hosts: all
  vars:
    domain: "auth.example.com"
    keycloak_version: "21.1.0"
    keycloak_administrator_username: "admin"
    keycloak_administrator_password: "securepassword"
    database_host: "db.example.com"
    database_name: "keycloak_db"
    database_username: "keycloak_user"
    database_password: "securedbpassword"
    http_port: 8080
    docker_restart_policy: "unless-stopped"
  roles:
    - docker-keycloak
```

## More Information 📚

For more details about Keycloak, check out:
- [Official Keycloak Documentation](https://www.keycloak.org/)
- [GitHub Repository](https://github.com/keycloak/keycloak)
- [Setting up Keycloak behind a Reverse Proxy](https://www.keycloak.org/server/reverseproxy)
- [Wikipedia](https://en.wikipedia.org/wiki/Keycloak)
- [Youtube Tutorial](https://www.youtube.com/watch?v=fvxQ8bW0vO8)
---

### Author ✍️
**Kevin Veen-Birkenbach**  
[veen.world](https://www.veen.world/)
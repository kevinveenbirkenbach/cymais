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

## Tasks 🛠️

The role performs the following main tasks:

1. **Include database and proxy configuration files:**
   - Integration of a PostgreSQL database.
   - Setup of a reverse proxy for the domain.

2. **Generate `docker-compose.yml`:**
   - Automatically generate the Docker Compose file based on templates and variables.

3. **Start Docker containers:**
   - The role launches the Keycloak project using Docker Compose.

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
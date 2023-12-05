# Docker MyBB Role

This README documents the Ansible role for setting up a MyBB forum using Docker. The role automates the deployment of MyBB, a free and open-source forum software, using Docker containers and manages the necessary configurations and dependencies.

## Role Name: Docker MyBB

### Dependencies
- nginx-docker-reverse-proxy

### Variables
- `docker_compose_instance_directory`: The directory where Docker Compose files for MyBB are stored.
- `conf_d_docker_directory`: Directory for Docker Nginx configuration.
- `default_conf_server_file`: The default Nginx configuration file for the server.
- `conf_d_server_directory`: The Nginx server's configuration directory.

### Tasks
1. **Domain Certificate Retrieval:** Automates the process of obtaining SSL certificates for the specified domain using Certbot.
2. **Nginx Configuration:** Handles the configuration of Nginx for the MyBB domain.
3. **Directory Creation:** Ensures the creation of necessary directories including parent directories as required.
4. **MyBB and Nginx Configuration:** Manages the configuration for MyBB and Nginx, including setting up the `default.conf` file.
5. **Docker Compose Setup:** Adds and manages the `docker-compose.yml` file necessary for running MyBB with Docker.

### Usage

#### Install Plugins 
To install MyBB plugins, extract them to a mounted volume and sync using the provided `docker run` command
```bash
docker run --rm -v mybb-data:/target/ -v /mnt/:/origin/ "kevinveenbirkenbach/alpine-rsync" sh -c "rsync -avv /origin/inc/plugins/ /target/"
```

#### Running the Role
Execute the Ansible playbook containing this role to set up MyBB in a Docker environment.

### Docker Compose Configuration
The `docker-compose.yml.j2` template outlines the services required for MyBB, including the application server, Nginx web server, and database (MariaDB).

### Additional Information
- For detailed configuration and customization, refer to the contents of the `default.conf` template and the `docker-compose.yml.j2` template.
- Ensure that the environment variables and paths are correctly set as per your system's configuration.

### Created with ChatGPT
This README was created with the assistance of ChatGPT, based on a conversation held at this [link](https://chat.openai.com/share/83828f9a-b817-48d8-86ed-599f64850b4d). ChatGPT provided guidance on structuring this document and outlining the key components of the Docker MyBB role.
# Docker Taiga Role 🐳📋

This Ansible role sets up and configures a Taiga project management platform using Docker. It includes tasks for setting up the database, Nginx proxy, and updating the repository with necessary files.

## Tasks

The main tasks included in this role are:

- Setting up the database.
- Configuring Nginx as a proxy.
- Updating the repository with necessary files.

## Variables

Key variables used in this role include the Docker Compose project name, database type and password, and the repository address.

## Templates

The role includes several Jinja2 templates to configure the environment and Docker Compose setup, including:

- **docker-compose-inits.yml.j2**
- **.env.j2**
- **docker-compose.yml.j2**

## Author

This role was created by Kevin Veen-Birkenbach. You can reach him at [kevin@veen.world](mailto:kevin@veen.world). Visit his website at [veen.world](https://www.veen.world/).

## Note

This README was created with the assistance of ChatGPT. [Link to conversation](https://chatgpt.com/share/fee718ab-cfe1-46f3-b97f-8f8c896ffd11).

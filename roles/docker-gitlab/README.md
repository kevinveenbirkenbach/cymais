# Docker-GitLab Ansible Role

## Overview
This Ansible role is designed for setting up and managing a GitLab server running in a Docker container. It automates the process of installing GitLab, configuring its environment, and managing dependencies such as a PostgreSQL database and an Nginx reverse proxy.

## Features
- **GitLab Installation**: Automatically deploys GitLab using Docker.
- **External PostgreSQL Database**: Configures GitLab to use an external PostgreSQL database.
- **Nginx Reverse Proxy Integration**: Includes tasks for setting up an Nginx reverse proxy for GitLab.
- **Customizable Configuration**: Variables and templates allow for easy customization.

## Requirements
- Docker and Docker Compose installed on the target machine.
- Ansible for automation.

## Role Variables
Variables are defined in `vars/main.yml`. Key variables include:
- `docker_compose_instance_directory`: Directory for Docker Compose instances.
- `database_instance`, `database_host`, `database_databasename`, `database_username`, `database_password`: Database configuration variables.
- `database_version`: PostgreSQL version, with a default fallback.

## Handlers
- `recreate gitlab`: Restarts GitLab using Docker Compose when changes are detected.

## Dependencies
- `nginx-docker-reverse-proxy`: A role for setting up an Nginx reverse proxy for GitLab.

## Template Files
- `docker-compose.yml.j2`: Jinja2 template for the Docker Compose configuration.
- Additional templates for database and proxy configuration.

## Usage
Include this role in your Ansible playbooks and specify the necessary variables. Run the playbook to deploy and configure GitLab in a Docker environment.

For a detailed walkthrough and explanation of this role, refer to the conversation at [ChatGPT Session Transcript](https://chat.openai.com/share/1b0147bf-d4de-4790-b8ed-c332aa4e3ce3).
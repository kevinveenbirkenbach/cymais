# README.md for Docker OpenProject Role

## Overview

This role is designed to deploy the OpenProject application using Docker. It includes tasks for setting up the environment, pulling the Docker repository, and configuring a reverse proxy with Nginx.

## Requirements

- Ansible
- Docker
- Docker Compose
- Access to the GitHub repository "opf/openproject-deploy"

## Role Variables

The role uses several variables, defined in `vars/main.yml`:

- `repository_directory`: The directory for the OpenProject repository.
- `docker_compose.directories.instance`: Directory for Docker Compose instances.

## Handlers

Defined in `handlers/main.yml`, the handler `recreate openproject` is used for recreating the OpenProject instance with specific environment settings.

## Tasks

Outlined in `tasks/main.yml`, the role includes tasks for:

- Including Nginx Docker proxy domain tasks.
- Creating the repository directory.
- Pulling the OpenProject Docker repository.
- Warning if the repository is not reachable.
- Copying the `.env` file from a template.

## Templates

`env.j2` in `templates/` folder is a Jinja2 template for the `.env` file, setting up environment variables for the OpenProject container.

## Dependencies

This role depends on `nginx-docker-reverse-proxy`, as defined in `meta/main.yml`.

## Usage

To use this role, include it in your Ansible playbook and set the necessary variables, especially those required in the `.env` file template.

## Notes

Ensure that Docker and Docker Compose are installed and configured correctly on the target machine. Also, ensure that the necessary ports are open and accessible.
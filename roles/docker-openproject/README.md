# OpenProject Role

## Overview

This role is designed to deploy the [OpenProject](https://www.openproject.org/) application using Docker. It includes tasks for setting up the environment, pulling the Docker repository, and configuring a reverse proxy with Nginx. It was developed by [Kevin Veen-Birkenbach](https://www.veen.world/)

## Handlers

Defined in `handlers/main.yml`, the handler `recreate openproject` is used for recreating the OpenProject instance with specific environment settings.

## Tasks

Outlined in `tasks/main.yml`, the role includes tasks for:

- Including Nginx Docker proxy domain tasks.
- Creating the repository directory.
- Pulling the OpenProject Docker repository.
- Warning if the repository is not reachable.
- Copying the `.env` file from a template.

## Usage

To use this role, include it in your Ansible playbook and set the necessary variables, especially those required in the `.env` file template.

## Notes

Ensure that Docker and Docker Compose are installed and configured correctly on the target machine. Also, ensure that the necessary ports are open and accessible.
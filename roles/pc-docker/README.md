# README for PC-Docker Playbook

## Overview
This playbook, `pc-docker`, is part of a larger collection housed within the `cymais` repository. It is specifically tailored for setting up Docker and Docker Compose on personal computers (PCs) used for development purposes. The primary goal is to facilitate a development environment on individual workstations rather than configuring servers for hosting or distributing Docker images.

## Contents
The `main.yml` file in the `pc-docker` role consists of two primary tasks:

1. **Install Docker**: This task uses the `community.general.pacman` module to install `docker` and `docker-compose` on the system. It ensures that these packages are present on the PC.

2. **User Group Configuration**: This task adds a specified user (denoted as `{{client_username}}`) to the Docker user group. This is crucial for allowing the specified user to interact with Docker without needing superuser permissions.

## Use Case
The playbook is designed for developers who require Docker in their local development environments. It simplifies the process of Docker installation and configuration, making it straightforward for developers to start containerizing their applications without the complexities often encountered in a server or production environment.

## Prerequisites
- Ansible: Ensure that Ansible is installed on your system to run this playbook.
- Arch Linux-based System: This playbook uses the `pacman` package manager, indicating it's designed for Arch Linux-based systems.

## Running the Playbook
To run this playbook:
1. Clone the `cymais` repository.
2. Navigate to the `roles/pc-docker` directory.
3. Run the playbook using the appropriate Ansible commands, ensuring that you have the necessary privileges.

## Important Notes
- **Not for Server Use**: This playbook is not designed for server environments. It is optimized for individual development machines.
- **Customization**: You may need to customize the playbook, especially the `{{client_username}}` variable, to suit your specific setup.
- **Security Considerations**: While adding a user to the Docker group provides ease of use, be aware of the security implications. It grants the user elevated privileges which, if misused, can affect the entire system.

## Support & Contribution
For support, suggestions, or contributions, please raise an issue or a pull request in the `cymais` repository. This project welcomes contributions from the developer community.
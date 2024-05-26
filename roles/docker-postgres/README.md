# Docker-Postgres Ansible Role

## Overview
This Ansible role is designed to deploy a PostgreSQL database using Docker. It includes tasks for setting up a Docker network, installing PostgreSQL in a Docker container, and initializing the database with a specified user and database.

## Role Variables
- `central_postgres_password`: The password for the PostgreSQL superuser (`postgres`).
- `database_name`: Name of the database to be created.
- `database_username`: Username for the database user.
- `database_password`: Password for the database user.

## Role Tasks
1. **Create Docker network for PostgreSQL**: Sets up a Docker network for PostgreSQL communication.
2. **Install PostgreSQL**: Deploys PostgreSQL in a Docker container, attaching it to the created network and setting the superuser password.
3. **Run the docker_postgres tasks once**: Ensures that the tasks are only run once to avoid redundancy.

## Handlers
- **Create database**: Creates a new database with the specified name.
- **Create database user**: Sets up a user with full privileges on the newly created database.

## Usage
1. Set the required variables in your playbook or inventory file.
2. Include this role in your playbook.
3. Run the playbook against the target host.

## Root Access
To access the database via the root account execute the following on the server:
```bash
docker exec -it central-postgres psql -U postgres
```

## Notes
- The PostgreSQL server is bound to `127.0.0.1:5432` on the host machine, making it accessible only from localhost.
- Ensure that the provided passwords are secure and stored securely, preferably using Ansible Vault or another encryption method.
# Database Docker Composition

This role combines the central RDBMS role (`cmp-rdbms-orchestrator`) with Docker Compose to deliver a ready-to-use containerized database environment.

## Features

- **Central RDBMS Integration**  
  Includes the `cmp-rdbms-orchestrator` role, which handles backups, restores, user and permission management for your relational database system (PostgreSQL, MariaDB, etc.).

- **Docker Compose**  
  Utilizes the standalone `docker-compose` role to define and bring up containers, networks, and volumes automatically.

- **Variable Load Order**  
  1. Docker Compose variables (`roles/docker-compose/vars/docker-compose.yml`)  
  2. Database variables (`roles/cmp-rdbms-orchestrator/vars/database.yml`)  
  Ensures compose ports and volumes are defined before the database role consumes them.

The role will load both sub-roles and satisfy all dependencies transparently.

## Task Breakdown

1. **Set Fact** `database_application_id` to work around lazy‐loading ordering.
2. **Include Vars** in the specified order.
3. **Invoke** `docker-compose` role to create containers, networks, and volumes.
4. **Invoke** `cmp-rdbms-orchestrator` role to provision the database, backups, and users.
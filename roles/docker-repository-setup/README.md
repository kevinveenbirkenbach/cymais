# Docker Repository Setup 🚀

This Ansible role sets up and manages your Docker repository. It ensures that the repository is pulled from your remote Git source, and it automatically triggers a rebuild of your Docker images using Docker Compose. 

## Features 🔧

- **Default Path Setup:**  
  Automatically sets a default `docker_repository_path`

- **Repository Management:**  
  Clones or updates your Docker repository from a specified Git repository.

- **Automated Build Trigger:**  
  Notifies handlers to rebuild the Docker repository using Docker Compose with extended timeouts.

## Role Structure 📂

- **Handlers:**  
  - `rebuild docker repository`: Runs `docker compose build` in the designated repository directory with custom timeout settings.

- **Tasks:**  
  - Sets the default repository path if undefined.
  - Pulls the latest code from the Docker repository.
  - Notifies the Docker Compose project setup and triggers a repository rebuild.

- **Meta:**  
  - Declares a dependency on the `docker-compose` role to ensure that handlers and related dependencies are loaded.

## Usage ⚙️

Ensure that you have set the following variables (either via your inventory, `group_vars`, or `host_vars`):

- `docker_repository_address`: The Git repository URL of your Docker repository.
- `docker_compose.directories.services`: The base directory where your Docker services are stored.  
  The role will append `repository/` to this path to form `docker_repository_path`.

## Author

Kevin Veen-Birkenbach  
[https://www.veen.world](https://www.veen.world)

---

Happy deploying! 🚀🐳
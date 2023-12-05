# Docker Listmonk Role

This role deploys the Listmonk application using Docker. Listmonk is a high performance, self-hosted newsletter and mailing list manager with a modern dashboard.

## Prerequisites
- Docker and Docker Compose should be installed on your system.
- Make sure that the required ports are available and not used by other services.

## Installation and Configuration

1. **Clone the Repository**:
   - Ensure you have the latest version of this playbook from the repository.

2. **Configure Variables**:
   - Set your desired configurations in `vars/main.yml`. This includes the path to your Docker Compose files and any other relevant variables.

3. **Run the Playbook**:
   - Execute the ansible playbook to set up Listmonk.

4. **Initial Database Setup**:
   - After the first setup, run the following command to initialize the Listmonk database:
     ```bash
     docker compose run --rm application ./listmonk --install
     ```

5. **Configure Reverse Proxy** (Optional):
   - If you are using a reverse proxy, configure it as per your domain settings in the `nginx-docker-reverse-proxy` role.

6. **Start Services**:
   - Use the following command to start Listmonk services:
     ```bash
     docker-compose -p listmonk up -d --force-recreate
     ```

## Configuration Files

- **docker-compose.yml**: Defines the Docker setup for Listmonk and its database.
- **config.toml**: Contains the application settings including the database connection, admin credentials, and server settings.

## Further Information
- For detailed installation instructions and configuration options, visit the [Listmonk Installation Documentation](https://listmonk.app/docs/installation/).
- You can also find more information on the [Listmonk GitHub Repository](https://github.com/knadh/listmonk/).

## Dependencies
- This role depends on `nginx-docker-reverse-proxy` for setting up a reverse proxy for Listmonk.

## Developed with AI
This Docker Listmonk role was developed with assistance from ChatGPT, a conversational AI by OpenAI. The conversation and guidance provided by ChatGPT can be found [here](https://chat.openai.com/share/95e722f5-3bd9-4203-8755-def2eca4796e).


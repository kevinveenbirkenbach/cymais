# Docker Listmonk Role

This role deploys the Listmonk application using Docker. Listmonk is a high performance, self-hosted newsletter and mailing list manager with a modern dashboard.

## Prerequisites
- Docker and Docker Compose should be installed on your system.
- Make sure that the required ports are available and not used by other services.

## Configuration Files

- **docker-compose.yml**: Defines the Docker setup for Listmonk and its database.
- **config.toml**: Contains the application settings including the database connection, admin credentials, and server settings.

## 📚 Other Resources
- For detailed installation instructions and configuration options, visit the [Listmonk Installation Documentation](https://listmonk.app/docs/installation/).
- You can also find more information on the [Listmonk GitHub Repository](https://github.com/knadh/listmonk/).

## Dependencies
- This role depends on `nginx-docker-reverse-proxy` for setting up a reverse proxy for Listmonk.

## Developed with AI
This Docker Listmonk role was developed with assistance from ChatGPT, a conversational AI by OpenAI. The conversation and guidance provided by ChatGPT can be found [here](https://chat.openai.com/share/95e722f5-3bd9-4203-8755-def2eca4796e).


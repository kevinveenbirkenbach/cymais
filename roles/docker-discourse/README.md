# Ansible Role: Docker-Discourse

This Ansible role sets up Discourse, a popular open-source discussion platform, using Docker containers. It is designed to automate the deployment and configuration process of Discourse, making it easier to maintain and update.

## Role Variables

- `docker_compose_instance_directory`: Specifies the directory for the Docker Compose instance of Discourse.

## Handlers

- `recreate discourse`: Rebuilds the Discourse application using the launcher script. Triggered when configuration changes are detected.

## Tasks

- Includes tasks from `nginx-docker-proxy-domain.yml`.
- Creates the specified `docker_compose_instance_directory`.
- Checks out the repository at the specified directory.
- Pulls the Discourse Docker repository and updates it.
- Sets permissions for the `containers` directory.
- Copies configuration to `containers/app.yml`.

## Template: app.yml.j2

- Configures the Discourse Docker container with necessary parameters such as database settings, environment variables, and volumes.
- Specifies SMTP settings for email functionality.

## Dependencies

- `nginx-docker-reverse-proxy`: This dependency is necessary for the reverse proxy setup for Discourse.

## Usage

To use this role, include it in your Ansible playbook and configure the necessary variables as per your requirements. Ensure that the dependencies are also resolved.

## Discussion and Contributions

For discussions, questions, and contributions related to this role, please refer to the corresponding discussion thread on [Discourse Meta](https://meta.discourse.org/).

## Notes

- This role is part of a larger playbook and is designed to work in conjunction with other roles.
- Ensure you have the necessary permissions and access to run Ansible scripts in your environment.

---

This README was generated with information provided in the Ansible role. For more detailed instructions and information, refer to the inline comments within the role files. Additional support and context for this role can be found in an [online chat discussion](https://chat.openai.com/share/fdbf9870-1f7e-491f-b4d2-357e6e8ad59c).


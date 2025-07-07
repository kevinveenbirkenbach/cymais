# Role: docker-container

## Description

This Ansible role supplies common Jinja2 snippets for composing Docker services consistently. Rather than repeating the same YAML blocks, you include one or more of the provided templates in your `docker-compose.yml.j2`.

## Overview

The following templates are available under `roles/docker-container/templates/`:

- **base.yml.j2**  
  Common service settings: `restart`, `env_file`, `logging`.

- **networks.yml.j2**  
  Conditional network attachments:
  - `central_<database_type>` when `central_database` feature is enabled  
  - `central_ldap` when LDAP feature and network are enabled  
  - `default`

- **depends_on_dmbs.j2**  
  Builds a `depends_on:` block automatically:
  - If `central_database` is **off**, renders an empty list `depends_on: []`  
  - Otherwise, includes `database` and/or `redis` with healthcheck conditions

- **healthcheck/**  
  Four strategies:
  - `curl.yml.j2` (HTTP via `curl -f`)  
  - `wget.yml.j2` (HTTP via `wget --spider`)  
  - `tcp.yml.j2`  (TCP socket test)  
  - `msmtp_curl.yml.j2` (SMTP first, then HTTP via `curl`; avoids duplicate emails)

Include whichever snippets your service requires to keep your Compose files DRY and maintainable.

## Features

- **Modular templates**  
  Mix only the blocks you need.

- **Feature‐driven logic**  
  Networks and dependencies adjust automatically based on your `applications` variables.

- **Multiple healthcheck options**  
  Pick the probe that works best for your container’s protocol and requirements.

## Further Resources

- [Docker Compose file reference](https://docs.docker.com/compose/compose-file/)  
- [Ansible variable precedence](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#understanding-variable-precedence)  
- [Jinja2 templating guide](https://jinja.palletsprojects.com/)  

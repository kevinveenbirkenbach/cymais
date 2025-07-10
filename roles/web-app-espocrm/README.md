# EspoCRM

## Description

Enhance your sales and service processes with EspoCRM, an open-source CRM featuring workflow automation, LDAP/OIDC single sign-on, and a sleek, lightweight UI! 🚀💼

## Overview

This Ansible role deploys EspoCRM using Docker. It handles:

- MariaDB database provisioning via the `cmp-rdbms-orchestrator` role  
- Nginx domain setup with WebSocket and reverse-proxy configuration  
- Environment variable management through Jinja2 templates  
- Docker Compose orchestration for **web**, **daemon**, and **websocket** services  
- Automatic OIDC scope configuration within the EspoCRM container  

With this role, you'll have a production-ready CRM environment that's secure, scalable, and real-time.

## Features

- **Workflow Automation:** Create and manage automated CRM processes with ease 🛠️  
- **LDAP/OIDC SSO:** Integrate with corporate identity providers for seamless login 🔐  
- **WebSocket Notifications:** Real-time updates via ZeroMQ and WebSockets 🌐  
- **Config via Templates:** Fully customizable `.env` and `docker-compose.yml` with Jinja2 ⚙️  
- **Health Checks & Logging:** Monitor service health and logs with built-in checks and journald 📈  
- **Modular Role Composition:** Leverages central roles for database and Nginx, ensuring consistency across deployments 🔄  

## Further Resources

- [EspoCRM Official Website](https://www.espocrm.com/) 🌍  
- [EspoCRM Documentation](https://docs.espocrm.com/) 📖  
- [CyMaIS Project Repository](https://github.com/kevinveenbirkenbach/cymais) 🔗  

## Credits

Developed and maintained by **Kevin Veen-Birkenbach**.  
Consulting & Coaching Solutions: [veen.world](https://www.veen.world) 🌟  
Part of the [CyMaIS Project](https://github.com/kevinveenbirkenbach/cymais) 📂  
License: [CyMaIS NonCommercial License (CNCL)](https://s.veen.world/cncl) ⚖️  

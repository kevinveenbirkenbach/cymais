# PeerTube

## Description

PeerTube is a decentralized, open‑source video hosting platform that empowers creators to share videos without relying on centralized services. It leverages federated architecture and peer-to-peer technologies to provide scalable, secure, and community‑driven video streaming.

## Overview

This Docker Compose deployment sets up PeerTube with integrated support for essential services such as a PostgreSQL database, Redis cache, and an Nginx reverse proxy for secure HTTPS termination and domain routing. The configuration supports advanced security settings, modular service scaling, and automated environment injection.

## Core Software Features

- **Decentralized Video Hosting:**  
  Distribute video hosting across multiple instances to enhance resilience and avoid single‑point control.

- **Scalability and Performance:**  
  Efficiently manage video transcoding, live streaming, and storage through containerized microservices.

- **Customizable Configuration:**  
  Tailor settings such as storage, email delivery, and administrative parameters using environment variables and configuration files.

- **Secure and Private:**  
  Built‑in support for TLS, secure SMTP integration, and strict administrative controls to ensure data protection.

- **Federated Communication:**  
  Designed to operate within a federated network, enabling seamless sharing and interconnection with other PeerTube instances.

## Documentation & Administration

- [Administration.md](./Administration.md)  
  Contains manual operations for container management, configuration updates, and administrative commands.

- [Upgrade.md](./Upgrade.md)  
  Provides guidance for upgrading your PeerTube deployment.

## Other Resources

- [PeerTube Official Documentation](https://docs.joinpeertube.org/install-docker)
- [PeerTube GitHub Issues](https://github.com/Chocobozzz/PeerTube/issues/3091)
- [OIDC Plugin Installation Guide](https://chatgpt.com/c/67a4f448-4be8-800f-8639-4c15cb2fb44e)

## Credits

Developed and maintained by **Kevin Veen-Birkenbach**  
Learn more at [www.veen.world](https://www.veen.world)

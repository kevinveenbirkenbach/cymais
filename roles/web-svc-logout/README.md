# web-svc-logout

This folder contains an Ansible role to deploy and configure the **Universal Logout Service**.

## Description

This role sets up the universal logout proxy service, a Dockerized Python Flask container that coordinates logout requests across multiple OIDC-integrated applications. It also configures the necessary Nginx proxy snippets and environment variables to enable unified logout flows.

It solves the common challenge of logging a user out from all connected apps with a single action, especially in environments where apps live on multiple subdomains and use OIDC authentication.

## Overview

- Deploys the universal logout service container based on the official [universal-logout GitHub repository](https://github.com/kevinveenbirkenbach/universal-logout).
- Configures the logout domains dynamically based on application inventory and features using custom Ansible filters.
- Provides an Nginx `/logout` proxy configuration snippet that handles CORS and forwards logout requests to the logout service.
- Supplies a user-friendly logout conductor UI that requests logout on all configured domains and shows live status.
- Designed to be used as the Front Channel Logout URL for Keycloak or other OpenID Connect providers, enabling a seamless, service-spanning logout experience.

## Features

- Automatic discovery of logout domains from applications with the `features.universal_logout` flag enabled.
- Centralized logout proxy that clears cookies and sessions across all configured subdomains.
- Status page with live feedback on logout progress for each domain.
- Built-in support for Docker Compose deployment and integration with the CyMaIS ecosystem.
- Includes security-conscious headers (CORS, CSP) for smooth cross-domain logout operations.

## Further Resources

- [Universal Logout GitHub Repository](https://github.com/kevinveenbirkenbach/universal-logout)  
- [CyMaIS Project](https://cymais.cloud)  
- [Author: Kevin Veen-Birkenbach](https://veen.world)  

---

*This role is licensed under the [CyMaIS NonCommercial License (CNCL)](https://s.veen.world/cncl).*

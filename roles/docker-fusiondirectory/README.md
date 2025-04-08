# DRAFT FusionDirectory DRAFT🐳

# TODO
This needs to be implemented

## Description

This Ansible role deploys and configures [FusionDirectory](https://www.fusiondirectory.org/) – a powerful web-based LDAP administration tool. Using Docker Compose, the role runs a pre-configured FusionDirectory container which allows you to manage your LDAP directory through a user-friendly web interface.

## Overview

Designed to simplify LDAP management, this role:
- Loads necessary FusionDirectory-specific variables.
- Generates an environment file based on a template.
- Deploys a FusionDirectory Docker container via Docker Compose.
- Integrates with your existing central LDAP service.

## Purpose

The purpose of this role is to automate the deployment of FusionDirectory in your Docker environment, ensuring a quick and consistent setup for managing your LDAP data. Ideal for production or homelab deployments, it reduces manual configuration steps and helps enforce best practices.

## Features

- **Easy Deployment:** Minimal manual setup via pre-configured templates and variables.
- **LDAP Integration:** Connects seamlessly with your existing central LDAP server.
- **Web Interface:** Provides an intuitive GUI for LDAP administration.
- **Docker Compose Integration:** Automates container creation and restart.

## Credits 📝

Developed and maintained by **Kevin Veen-Birkenbach**.  
Learn more at [www.veen.world](https://www.veen.world)  
Part of the [CyMaIS Project](https://github.com/kevinveenbirkenbach/cymais)  
License: [CyMaIS NonCommercial License (CNCL)](https://s.veen.world/cncl)
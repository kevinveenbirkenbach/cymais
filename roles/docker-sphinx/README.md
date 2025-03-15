# Sphinx Documentation Role

## Description

This Ansible role automates the building and deployment of Sphinx documentation using Docker. It pulls the CyMaIS repository, builds the documentation with Sphinx, and serves the generated HTML files via a lightweight HTTP server.

## 📌 Overview

Optimized for containerized environments, this role ensures that your documentation is consistently built and deployed with minimal manual intervention. It leverages Docker and Docker Compose for reproducible builds, enabling dynamic configuration of source and output directories.

## Purpose

The primary purpose of this role is to streamline the documentation workflow for your project. By automating the Sphinx build process and containerizing the deployment, the role reduces manual overhead and ensures that the latest documentation is always available for review and distribution.

## Features

- **Automated Build:** Triggers the Sphinx build process automatically via a Makefile.
- **Docker Integration:** Uses Docker and Docker Compose to containerize the documentation build and serve process.
- **Dynamic Configuration:** Allows customizable source and output directories through variables.
- **Consistent Deployment:** Ensures that the generated documentation is served reliably with minimal configuration.
- **Easy Updates:** Pulls the latest version of the project repository and rebuilds the documentation seamlessly.

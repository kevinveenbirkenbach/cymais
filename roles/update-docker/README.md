# Update Docker

## Description

This role updates Docker Compose instances by checking for changes in Docker image digests and applying updates if necessary. It utilizes a Python script to handle git pulls and Docker image pulls, and rebuilds containers when changes are detected.

## 📌 Overview

The role performs the following:
- Deploys a Python script to check for Docker image updates.
- Configures a systemd service to run the update script.
- Restarts the Docker update service upon configuration changes.
- Supports additional procedures for specific Docker applications (e.g., Discourse, Mastodon, Nextcloud).

## Purpose

The role is designed to ensure that Docker images remain current by automatically detecting changes and rebuilding containers as needed. This helps maintain a secure and efficient container environment.

## Features

- **Docker Image Monitoring:** Checks for changes in image digests.
- **Automated Updates:** Pulls new images and rebuilds containers when necessary.
- **Service Management:** Configures and restarts a systemd service to handle updates.
- **Application-Specific Procedures:** Includes hooks for updating specific Docker applications.

## Credits 📝
It was created with the help of ChatGPT. The conversation is available [here](https://chat.openai.com/share/165418b8-25fa-433b-baca-caded941e22a)
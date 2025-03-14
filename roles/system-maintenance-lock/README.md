# System Maintenance Lock

## Description

This role provides a locking mechanism to ensure that critical services are not interrupted during maintenance activities such as updates, backups, or patch applications. It waits for specified services to stop and prevents conflicting operations.

## 📌 Overview

The role performs the following:
- Blocks execution until specified services have stopped.
- Implements retry logic with a configurable timeout.
- Ensures that maintenance tasks are executed only when the system is in a safe state.

## Purpose

The primary purpose of this role is to safeguard system stability during maintenance by preventing conflicts with running services. It ensures that maintenance operations proceed only when the environment is ready.

## Features

- **Service Locking:** Blocks maintenance tasks until critical services are stopped.
- **Timeout and Retry Logic:** Configurable wait times and maximum attempts.
- **Conflict Avoidance:** Prevents interference between maintenance operations and running services.

## Credits 📝
Created with ChatGPT. Conversation is [here](https://chat.openai.com/share/a886b86b-8de6-4eca-9fba-e36c9f20d536) available.
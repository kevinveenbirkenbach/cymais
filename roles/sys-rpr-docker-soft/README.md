# Docker Healer 🩺

## Description

This Ansible role automatically restarts Docker Compose configurations with exited or unhealthy containers on Arch Linux systems. It ensures the stability of containerized workloads by recovering from common error conditions like port binding issues.  

## Overview

Tailored for Arch Linux, this role monitors containers for failure states and initiates a controlled restart of affected Compose configurations. If port conflicts prevent recovery, the role stops the affected stack, restarts Docker, and recreates the container environment.

## Purpose

The purpose of this role is to provide automated healing for Docker Compose environments, minimizing manual recovery effort and reducing downtime.

## Features

- **Container Health Monitoring:** Detects unhealthy or exited containers.
- **Automated Recovery:** Restarts failed containers and resolves port binding issues.
- **Run-once Setup Logic:** Ensures idempotent execution by controlling task flow with internal flags.
- **System Role Integration:** Seamlessly integrates with CyMaIS system maintenance logic.

## Credits 📝

Developed and maintained by **Kevin Veen-Birkenbach**.  
Learn more at [www.veen.world](https://www.veen.world)

Part of the [CyMaIS Project](https://github.com/kevinveenbirkenbach/cymais)  
License: [CyMaIS NonCommercial License (CNCL)](https://s.veen.world/cncl)

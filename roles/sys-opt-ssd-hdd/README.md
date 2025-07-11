# Storage Optimizer

## Description

This role optimizes storage allocation for Docker volumes by migrating volumes between SSD (rapid storage) and HDD (mass storage) based on container image types. It creates symbolic links to maintain consistent storage paths after migration.

## Overview

The role performs the following tasks:
- Migrates Docker volumes with database workloads to rapid storage (SSD) for improved performance.
- Moves non-database Docker volumes to mass storage (HDD) to optimize storage usage.
- Manages container stopping and restarting during the migration process.
- Creates symbolic links to preserve consistent file paths.

## Purpose

The primary purpose of this role is to enhance system performance by ensuring that Docker volumes are stored on the most appropriate storage medium, optimizing both speed and capacity.

## Features

- **Dynamic Volume Migration:** Moves Docker volumes based on container image types.
- **Symbolic Link Creation:** Maintains consistent access paths after migration.
- **Container Management:** Safely stops and starts containers during volume migration.
- **Performance Optimization:** Improves overall system performance by leveraging appropriate storage media.

## Credits 📝

For detailed context and the development history of this role, refer to [this conversation](https://chat.openai.com/share/40fef8a6-5e9b-4b5e-8e68-7f2fd9abf5cc).


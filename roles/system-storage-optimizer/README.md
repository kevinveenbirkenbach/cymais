# System Storage Optimizer Role

## Overview

The `system-storage-optimizer` role is designed for managing and optimizing storage allocation of Docker volumes. It automates the process of moving Docker volumes between SSD (rapid storage) and HDD (mass storage) based on the container image types, enhancing performance and efficiency.

## Features

- Dynamically moves Docker volumes based on container image types.
- Utilizes SSDs for database-related volumes for faster access.
- Moves non-database volumes to HDDs for efficient mass storage.
- Handles container stopping and starting during the optimization process.
- Creates symbolic links to maintain consistent paths.


## Usage

To deploy this role, include it in your Ansible playbook and define the necessary paths for SSD and HDD storage.

## Additional Information

For detailed context and the development history of this role, refer to [this conversation](https://chat.openai.com/share/40fef8a6-5e9b-4b5e-8e68-7f2fd9abf5cc).


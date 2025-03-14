# PC-Streaming-Tools Role

## 📌 Overview
This README is associated with the `pc-streaming-tools` role, part of the `cymais` repository. This role is focused on setting up essential tools for live streaming and video recording on personal computers.

## Role Tasks
The `main.yml` file in the `pc-streaming-tools` role includes a task for installing a key streaming software:

1. **Install Streaming**:
   - The role uses the `community.general.pacman` module to install:
     - `obs-studio`: Open Broadcaster Software Studio, a free and open-source software for video recording and live streaming.

## Purpose and Usage
The `pc-streaming-tools` role is designed for content creators, gamers, educators, and anyone who needs to record video or stream live content. OBS Studio provides a versatile platform for video production and live streaming, offering features like high-performance real-time video/audio capturing and mixing.

## Prerequisites
- **Ansible**: Required for running this role.
- **Arch Linux-based System**: As the role employs the `pacman` package manager, it is tailored for systems based on Arch Linux or similar distributions.

## Running the Role
To use this role:
1. Clone the `cymais` repository.
2. Navigate to the `roles/pc-streaming-tools` directory.
3. Run the role using Ansible, ensuring you have the necessary permissions for software installation.

## Customization
This role primarily focuses on installing OBS Studio, but you can customize it by adding additional streaming or video recording tools as per your requirements.

## Support and Contributions
For support, feedback, or contributions, such as adding more streaming tools or enhancing the existing setup, please open an issue or submit a pull request in the `cymais` repository. Contributions that enhance the streaming capabilities of this role are highly welcome.
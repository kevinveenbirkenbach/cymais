# System Btrfs Auto Balancer Role 📦

This Ansible role automates the management and balancing of Btrfs file systems. It ensures that the Btrfs file system is maintained efficiently without manual intervention.

## Features ✨

- **Automatic Cloning of Repository:** Fetches the latest `auto-btrfs-balancer` repository from GitHub.
- **Systemd Service Configuration:** Creates and configures a Systemd service to automatically run the balancing script.
- **Systemd Timer Integration:** Integrates a Systemd timer to run the balancing service at regular intervals.
- **Error Notification:** Notifies via Systemd in case of errors during the balancing process.

## Prerequisites 📋

- **Ansible:** This role requires Ansible to run.
- **Systemd:** Target systems must support Systemd.
- **Git:** Git must be installed to clone the repository.


## Author ✍️

This role was created by [Kevin Veen-Birkenbach](https://www.veen.world).
- **Email:** kevin@veen.world
- **Website:** [veen.world](https://www.veen.world)

## Contact ☎️

For questions or support, you can reach Kevin Veen-Birkenbach via [email](mailto:kevin@veen.world).

## Created with AI
This README.md was created with the assistance of ChatGPT. You can view the conversation [here](https://chatgpt.com/share/dcec1b4a-c7a8-4cf8-a87a-987eb0500857).

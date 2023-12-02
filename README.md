# CyMaIS - Cyber Master Infrastructure Solution
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

This playbook, powered by Ansible, is designed to streamline the setup and administration of a wide range of applications and Docker images on Linux-based systems. It's a versatile tool for configuring both bare metal servers and personal computers, offering solutions for base system setup, administration tools, backup solutions, system monitoring, updates, driver management, security enhancements, VPN configurations, and more. Whether for desktop computing, development environments, server management, or Docker containerization, this playbook provides comprehensive and customizable Ansible roles for efficient system management.

## CyMaIS Implementation
If you're seeking professional implementation of the **CyMaIS - Cyber Master Infrastructure Solution** and its components, look no further. I offer tailored software development, infrastructure setup, and security solutions, particularly for small and medium-sized businesses. My expertise spans various areas, including server administration, digital corporate infrastructure, custom software development, and information security. With a strong focus on Open Source solutions, I ensure that your IT infrastructure aligns with the highest industry standards. For more detailed information about my services and how I can assist in optimizing your IT environment, please visit [CyberMaster.Space](https://cybermaster.space).

## Integrated Solutions

### Base Setup

Provides essential configurations for system initialization, including hostname setting, systemd journal management, locale configurations, and swapfile handling.

- **[Hostname](./roles/hostname/README.md)**: Sets the system's hostname.
- **[Journalctl](./roles/journalctl/README.md)**: Configures systemd journal settings.
- **[Locales](./roles/locales/README.md)**: Configures system locales.
- **[System-Swapfile](./roles/system-swapfile/README.md)**: Configures swapfile creation and management.

### Administration Tools

Includes necessary tools for effective system administration, such as Git setup, Linux admin tools, and sudo configuration.

- **[Git](./roles/git/)**: Basic Git version control system setup.
- **[PC-Administrator-Tools](./roles/pc-administrator-tools/README.md)**: Installs basic Linux administration tools.
- **[Sudo](./roles/sudo/README.md)**: Installs and configures sudo.

### Backup Solutions
Focuses on comprehensive backup strategies and cleanup procedures, encompassing data backups, remote server backups, and maintenance of backup storage efficiency.

#### Backups
- **[backup-data-to-usb](./roles/backup-data-to-usb/README.md)**: Automates data backup to USB devices.
- **[backup-docker-to-local](./roles/backup-docker-to-local/README.md)**: Backs up Docker volumes to local storage.
- **[backup-remote-to-local](./roles/backup-remote-to-local/README.md)**: Pulls backups from remote servers for local storage.
- **[backups-provider](./roles/backups-provider/README.md)**: Manages backup processes and storage solutions.
- **[backups-provider-user](./roles/backups-provider-user/README.md)**: Creates and configures users for backup processes.

#### Backups Cleanup
- **[cleanup-backups-service](./roles/cleanup-backups-service/README.md)**: Service to clean up old backups automatically.
- **[cleanup-backups-timer](./roles/cleanup-backups-timer/README.md)**: Timer for scheduling the backup cleanup service.
- **[cleanup-disc-space](./roles/cleanup-disc-space/README.md)**: Manages and frees up disk space on the system.
- **[cleanup-failed-docker-backups](./roles/cleanup-failed-docker-backups/README.md)**: Cleans up failed Docker backups.

### Monitoring

#### Notifier
Introduces roles for setting up system event notifications, with options for email and Telegram alerts.
- **[Systemd-Notifier](./roles/systemd-notifier/README.md)**: Notifier service for systemd.
- **[Systemd-Notifier-Email](./roles/systemd-notifier-email/README.md)**: Email notifications for systemd services.
- **[Systemd-Notifier-Telegram](./roles/systemd-notifier-telegram/README.md)**: Telegram notifications for systemd services.

#### Server Health
Addresses server maintenance and health monitoring, ensuring optimal performance and reliability of the server infrastructure.
- **[Health Btrfs](./roles/health-btrfs/)**: Monitors the health of Btrfs filesystems.
- **[Health Disc Space](./roles/health-disc-space/)**: Checks for available disk space.
- **[Health Docker Container](./roles/health-docker-container/)**: Monitors the health of Docker containers.
- **[Health Docker Volumes](./roles/health-docker-volumes/)**: Checks the status of Docker volumes.
- **[Health Journalctl](./roles/health-journalctl/)**: Monitors and manages the system journal.
- **[Health Nginx](./roles/health-nginx/)**: Ensures the Nginx server is running smoothly.
- **[Heal Docker](./roles/heal-docker/)**: Automated healing and maintenance tasks for Docker.

### Update
Covers automated updates and maintenance for the system and its components, including package managers and Docker containers.
- **[update](./roles/update/README.md)**: Automates the process of system updates.
- **[update-apt](./roles/update-apt/README.md)**: Updates system packages using apt (for Debian-based systems).
- **[update-docker](./roles/update-docker/README.md)**: Keeps Docker containers up to date.
- **[update-pacman](./roles/update-pacman/README.md)**: Updates system packages using Pacman (for Arch-based systems).

### Driver
Deals with the installation and configuration of various hardware drivers, catering to a range of devices and needs.
- **[driver-epson-multiprinter](./roles/driver-epson-multiprinter/README.md)**: Installs drivers for Epson multi-function printers.
- **[driver-intel](./roles/driver-intel/README.md)**: Installs Intel drivers, typically for graphics and other hardware.
- **[driver-msi-keyboard-color](./roles/driver-msi-keyboard-color/README.md)**: Configures MSI keyboard color settings.
- **[driver-non-free](./roles/driver-non-free/README.md)**: Installs non-free drivers, generally for specific hardware needs.

### Security
Enhances system security through roles focused on security measures, swap file management, user configurations, and SSH settings.
- **[System Security](./roles/system-security/)**: Enhances overall system security.
- **[System Swapfile](./roles/system-swapfile/)**: Manages swap files for system memory.
- **[User Administrator](./roles/user-administrator/)**: Setup for system administrator user.
- **[User Alarm](./roles/user-alarm/)**: Manages the alarm user.
- **[PC SSH](./roles/pc-ssh/)**: Configuration of SSH for secure remote access.
- **[SSHD](./roles/sshd/README.md)**: Configures SSH daemon settings.

### Virtual Private Network (VPN)
Centers on VPN configurations, specifically for Wireguard, providing secure and efficient network connectivity.
- **[client-wireguard](./roles/client-wireguard/README.md)**: Configures Wireguard VPN client.
- **[client-wireguard-behind-firewall](./roles/client-wireguard-behind-firewall/README.md)**: Sets up Wireguard client functionality behind a firewall.
- **[wireguard](./roles/wireguard/README.md)**: Installs and configures Wireguard for secure VPN connections.


### Desktop and Personal Computing
Offers a range of tools and software to enhance the personal computing experience on desktops and laptops, covering multimedia, productivity, and virtualization.
- **[PC Bluray Player Tools](./roles/pc-bluray-player-tools/)**: Software for playing Blu-ray media on personal computers.
- **[PC Caffeine](./roles/pc-caffeine/)**: Utility to keep your computer awake.
- **[PC Designer Tools](./roles/pc-designer-tools/)**: Graphic design and 3D modeling software.
- **[PC Games](./roles/pc-games/)**: Installation of various computer games.
- **[PC Gnome](./roles/pc-gnome/)**: Installation and configuration of Gnome desktop environment.
- **[PC LibreOffice](./roles/pc-libreoffice/)**: Installation of the LibreOffice suite.
- **[PC Network Analyze Tools](./roles/pc-network-analyze-tools/)**: Network analysis and troubleshooting utilities.
- **[PC Nextcloud](./roles/pc-nextcloud/)**: Client setup for Nextcloud cloud storage service.
- **[PC Office](./roles/pc-office/)**: Various office productivity tools.
- **[PC Qbittorrent](./roles/pc-qbittorrent/)**: Installation of qBittorrent for file sharing.
- **[PC Spotify](./roles/pc-spotify/)**: Installation of Spotify for music streaming.
- **[PC Streaming Tools](./roles/pc-streaming-tools/)**: Software for video streaming and recording.
- **[PC Torbrowser](./roles/pc-torbrowser/)**: Installation of Tor Browser for anonymous browsing.
- **[PC Video Conference](./roles/pc-video-conference/)**: Video conferencing software setup.
- **[PC Virtual Box](./roles/pc-virtual-box/)**: VirtualBox setup for creating virtual machines.

### Development Environment
Targets software developers with tools and environments for various programming languages and development needs.
- **[PC Developer Tools](./roles/pc-developer-tools/)**: Basic developer tools setup.
- **[PC Developer Tools Arduino](./roles/pc-developer-tools-arduino/)**: Setup for Arduino development.
- **[PC Developer Tools Bash](./roles/pc-developer-tools-bash/)**: Tools for Bash scripting.
- **[PC Developer Tools Java](./roles/pc-developer-tools-java/)**: Java development environment setup.
- **[PC Developer Tools PHP](./roles/pc-developer-tools-php/)**: PHP development environment setup.
- **[PC Developer Tools Python](./roles/pc-developer-tools-python/)**: Python development environment setup.

### Other
Encompasses miscellaneous essential tools and systems, including AUR helper, spellchecking, typesetting, and package management.
- **[System-Aur-Helper](./roles/system-aur-helper/README.md)**: Installs and configures AUR helper (yay).
- **[Hunspell](./roles/hunspell/)**: Installation of Hunspell spellchecker.
- **[Latex](./roles/latex/)**: Installation of LaTeX typesetting system.
- **[Java](./roles/java/README.md)**: Installs Java Development Kit (JDK).
- **[Python Pip](./roles/python-pip/)**: Installation of Python Pip package manager.

## Server

### Webserver
Focuses on web server roles and applications, covering SSL certificates, Nginx configurations, reverse proxies, and email services.
- **[Letsencrypt](./roles/letsencrypt/README.md)**: Configures Let's Encrypt for SSL certificates.
- **[Nginx](./roles/nginx/README.md)**: Installs and configures Nginx web server.
- **[Nginx-Docker-Reverse-Proxy](./roles/nginx-docker-reverse-proxy/README.md)**: Sets up a reverse proxy for Docker containers.
- **[Nginx-Homepage](./roles/nginx-homepage/README.md)**: Configures a homepage for Nginx.
- **[Nginx-Https](./roles/nginx-https/README.md)**: Enables HTTPS configuration for Nginx.
- **[Nginx-Matomo-Tracking](./roles/nginx-matomo-tracking/README.md)**: Integrates Matomo tracking with Nginx.
- **[Nginx-Redirect](./roles/nginx-redirect/README.md)**: Manages URL redirects in Nginx.
- **[Certbot Nginx](./roles/certbot-nginx/)**: Integrates Certbot with Nginx for SSL certificates.
- **[Postfix](./roles/postfix/)**: Setup for the Postfix mail transfer agent.

### Docker and Containerization
Dedicated to Docker container setups and application management, offering a wide array of software deployment options.
- **[Docker](./roles/docker/)**: Basic Docker and Docker Compose setup.
- **[Docker Akaunting](./roles/docker-akaunting/)**: Deployment of the Akaunting finance software.
- **[Docker Attendize](./roles/docker-attendize/)**: Setup for the Attendize event management tool.
- **[Docker Baserow](./roles/docker-baserow/)**: Deployment of Baserow, an open-source no-code database tool.
- **[Docker BigBlueButton](./roles/docker-bigbluebutton/)**: Setup for the BigBlueButton video conferencing tool.
- **[Docker ELK](./roles/docker-elk/)**: Elasticsearch, Logstash, and Kibana (ELK) stack setup.
- **[Docker Funkwhale](./roles/docker-funkwhale/)**: Deployment of Funkwhale, a federated music streaming server.
- **[Docker Gitea](./roles/docker-gitea/)**: Setup for the Gitea git server.
- **[Docker Jenkins](./roles/docker-jenkins/)**: Jenkins automation server setup.
- **[Docker Joomla](./roles/docker-joomla/)**: Joomla content management system setup.
- **[Docker Listmonk](./roles/docker-listmonk/)**: Setup for Listmonk, a self-hosted newsletter and mailing list manager.
- **[Docker Mailu](./roles/docker-mailu/)**: Complete mail server solution.
- **[Docker Mastodon](./roles/docker-mastodon/)**: Deployment of the Mastodon social network server.
- **[Docker Matomo](./roles/docker-matomo/)**: Setup for Matomo, an open-source analytics platform.
- **[Docker MediaWiki](./roles/docker-mediawiki/)**: MediaWiki setup for creating wikis.
- **[Docker MyBB](./roles/docker-mybb/)**: Setup for MyBB forum software.
- **[Docker Nextcloud](./roles/docker-nextcloud/)**: Cloud storage solution setup.
- **[Docker Peertube](./roles/docker-peertube/)**: Deployment of the PeerTube video platform.
- **[Docker Pixelfed](./roles/docker-pixelfed/)**: Pixelfed, a federated image sharing platform, setup.
- **[Docker Roulette Wheel](./roles/docker-roulette-wheel/)**: Setup for a custom roulette wheel application.
- **[Docker Wordpress](./roles/docker-wordpress/)**: Wordpress blog and website platform setup.
- **[Docker YOURLS](./roles/docker-yourls/)**: Setup for YOURLS, a URL shortening service.

### Setup

Run:
```bash
ansible-galaxy collection install -r requirements.yml
```

## Addidional Parameters

- activate_all_timers (bool): Activates matomo tracking on all html pages
- nginx_matomo_tracking_active (bool): Activates matomo tracking on all html pages

The role specific parameters are descriped in the README.md of the roles

## Author

Kevin Veen-Birkenbach  
- 📧 Email: [kevin@veen.world](mailto:kevin@veen.world)
- 🌍 Website: [https://www.veen.world/](https://www.veen.world/)

## License

This project is licensed under the GNU Affero General Public License v3.0. The full license text is available in the `LICENSE` file of this repository. 

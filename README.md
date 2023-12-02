# Computer Playbook
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Ansible software to setup and administrate applications and docker images on Linux computers. 

With this tool you can setup all of the following application on bare metal servers and personal computers

## Solutions

### Base Setup
- **[Hostname](./roles/hostname/README.md)**: Sets the system's hostname.
- **[Journalctl](./roles/journalctl/README.md)**: Configures systemd journal settings.
- **[Locales](./roles/locales/README.md)**: Configures system locales.
- **[System-Swapfile](./roles/system-swapfile/README.md)**: Configures swapfile creation and management.

### Administration Tools
- **[Git](./roles/git/)**: Basic Git version control system setup.
- **[PC-Administrator-Tools](./roles/pc-administrator-tools/README.md)**: Installs basic Linux administration tools.
- **[Sudo](./roles/sudo/README.md)**: Installs and configures sudo.

### Backup Solutions

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

### Notifier
- **[Systemd-Notifier](./roles/systemd-notifier/README.md)**: Notifier service for systemd.
- **[Systemd-Notifier-Email](./roles/systemd-notifier-email/README.md)**: Email notifications for systemd services.
- **[Systemd-Notifier-Telegram](./roles/systemd-notifier-telegram/README.md)**: Telegram notifications for systemd services.

### Update
- **[update](./roles/update/README.md)**: Automates the process of system updates.
- **[update-apt](./roles/update-apt/README.md)**: Updates system packages using apt (for Debian-based systems).
- **[update-docker](./roles/update-docker/README.md)**: Keeps Docker containers up to date.
- **[update-pacman](./roles/update-pacman/README.md)**: Updates system packages using Pacman (for Arch-based systems).

### Driver
- **[driver-epson-multiprinter](./roles/driver-epson-multiprinter/README.md)**: Installs drivers for Epson multi-function printers.
- **[driver-intel](./roles/driver-intel/README.md)**: Installs Intel drivers, typically for graphics and other hardware.
- **[driver-msi-keyboard-color](./roles/driver-msi-keyboard-color/README.md)**: Configures MSI keyboard color settings.
- **[driver-non-free](./roles/driver-non-free/README.md)**: Installs non-free drivers, generally for specific hardware needs.

### Security
- **[System Security](./roles/system-security/)**: Enhances overall system security.
- **[System Swapfile](./roles/system-swapfile/)**: Manages swap files for system memory.
- **[User Administrator](./roles/user-administrator/)**: Setup for system administrator user.
- **[User Alarm](./roles/user-alarm/)**: Manages the alarm user.
- **[PC SSH](./roles/pc-ssh/)**: Configuration of SSH for secure remote access.
- **[Sshd](./roles/sshd/README.md)**: Configures SSH daemon settings.

### Virtual Private Network
- **[client-wireguard](./roles/client-wireguard/README.md)**: Configures Wireguard VPN client.
- **[client-wireguard-behind-firewall](./roles/client-wireguard-behind-firewall/README.md)**: Sets up Wireguard client functionality behind a firewall.
- **[wireguard](./roles/wireguard/README.md)**: Installs and configures Wireguard for secure VPN connections.


### Desktop and Personal Computing
Tools and software enhancing personal computing on desktops or laptops:

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
Tools and environments for software development.
- **[PC Developer Tools](./roles/pc-developer-tools/)**: Basic developer tools setup.
- **[PC Developer Tools Arduino](./roles/pc-developer-tools-arduino/)**: Setup for Arduino development.
- **[PC Developer Tools Bash](./roles/pc-developer-tools-bash/)**: Tools for Bash scripting.
- **[PC Developer Tools Java](./roles/pc-developer-tools-java/)**: Java development environment setup.
- **[PC Developer Tools PHP](./roles/pc-developer-tools-php/)**: PHP development environment setup.
- **[PC Developer Tools Python](./roles/pc-developer-tools-python/)**: Python development environment setup.

### Other
- **[System-Aur-Helper](./roles/system-aur-helper/README.md)**: Installs and configures AUR helper (yay).
- **[Hunspell](./roles/hunspell/)**: Installation of Hunspell spellchecker.
- **[Latex](./roles/latex/)**: Installation of LaTeX typesetting system.
- **[Java](./roles/java/README.md)**: Installs Java Development Kit (JDK).
- **[Python Pip](./roles/python-pip/)**: Installation of Python Pip package manager.

## Server

### Webserver
Roles for web servers and related applications.
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
Setting up Docker containers and managing applications.

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

## Server Health
- **[Health Btrfs](./roles/health-btrfs/)**: Monitors the health of Btrfs filesystems.
- **[Health Disc Space](./roles/health-disc-space/)**: Checks for available disk space.
- **[Health Docker Container](./roles/health-docker-container/)**: Monitors the health of Docker containers.
- **[Health Docker Volumes](./roles/health-docker-volumes/)**: Checks the status of Docker volumes.
- **[Health Journalctl](./roles/health-journalctl/)**: Monitors and manages the system journal.
- **[Health Nginx](./roles/health-nginx/)**: Ensures the Nginx server is running smoothly.
- **[Heal Docker](./roles/heal-docker/)**: Automated healing and maintenance tasks for Docker.

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

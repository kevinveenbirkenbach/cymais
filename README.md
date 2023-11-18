# Computer Playbook
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Ansible software to setup and administrate applications and docker images on Linux computers. 

With this tool you can setup all of the following application on bare metal servers and personal computers

## Bare Metal Servers

### Included Applications

#### Docker Applications

This software allows to setup the docker following applications:

- [Nextcloud](./roles/docker-nextcloud/README.md) - Cloud Software
- [Akaunting](./roles/docker-akaunting/README.md) - Business Controlling Software
- [Big Blue Button](./roles/docker-bigbluebutton/README.md) - Video Conference Software
- [Gitea](./roles/docker-gitea/README.md) - Version Controll Software
- [Joomla](./roles/docker-joomla/) - CMS Software
- [Mailu](./roles/docker-mailu/README.md) - Mailsoftware 
- [Peertube](./roles/docker-peertube/README.md) - Video Platform Software
- [pixelfed](./roles/docker-pixelfed/README.md) - Photo Platform Software
- [Wordpress](./roles/docker-wordpress/README.md) - Blog Software
- [YOURLS](./roles/docker-yourls/README.md) - URL Shortening Software
- [Mastodon](./roles/docker-mastodon/README.md) - Micro Blog Software
- [Media Wiki](./roles/docker-mediawiki/README.md) - Wiki Software
- [MyBB](./roles/docker-mybb/README.md) - Forum Software

#### Native Applications

This software shipts the following tools which are natively setup on the server:
- [Backups Cleanup](./roles/cleanup-backups-timer/README.md) - Cleans up old backups
- [Btrfs Health Check](./roles/health-btrfs/README.md) - Checks the health of Btrfs file systems
- [Docker Health Check](./roles/health-docker-container/) - Checks the health of docker containers
- [Docker Reverse Proxy](./roles/nginx-docker-reverse-proxy/README.md) - Docker Reverse Proxy Solution
- [Docker Volume Backup](./roles/backup-docker-to-local/) - Backup Solution for Docker Volumes
- [Pull Primary Backups](./roles/backup-remote-to-local/README.md) - Pulls the backups from another server and stores them
- [Wireguard](./roles/wireguard/README.md) - Integrates the server in an wireguard vpn

## Personal Computers

This playbooks offers the setup of Manjaro GNOME clients.

### Included Applications
- [Basic Linux Administration Tools](./roles/collection-administrator-base/)
- [Network Analyzes Tools](./roles/collection-administrator-network-analyze/)
- [Designer Tools](./roles/collection-designer/)
- [Arduino Developer Tools](./roles/collection-developer-arduino/)
- [Basic Developer Tools](./roles/collection-developer-base/)
- [Bash Developer Tools](./roles/collection-developer-bash/)
- [Java Developer Tools](./roles/collection-developer-java/)
- [PHP Developer Tools](./roles/collection-developer-php/)
- [Python Developer Tools](./roles/collection-developer-python/)
- [Entertainment Software](./roles/collection-entertainment/)
- [Games](./roles/collection-games/)
- [Office Tools](./roles/collection-office/)
- [Streaming Tools](./roles/collection-streamer/)
- [Torrent Software](./roles/collection-torrent/)
- ...

### Setup

Run:
```bash
ansible-galaxy collection install -r requirements.yml
```

## Addidional Parameters

- activate_all_timers (bool): Activates matomo tracking on all html pages
- nginx_matomo_tracking_active (bool): Activates matomo tracking on all html pages

The role specific parameters are descriped in the readme.md of the roles

## Author

Kevin Veen-Birkenbach  
- 📧 Email: [kevin@veen.world](mailto:kevin@veen.world)
- 🌍 Website: [https://www.veen.world/](https://www.veen.world/)

## License

This project is licensed under the GNU Affero General Public License v3.0. The full license text is available in the `LICENSE` file of this repository. 

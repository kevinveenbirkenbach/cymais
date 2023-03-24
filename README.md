# Server-Playbook
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Ansible software to setup and administrate applications and docker images on Linux servers. 
With this tool you can setup all of the following application on an root dedicated server in less then 4 hours. 

## Included Applications

### Docker Applications

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

### Native Applications

This software shipts the following tools which are natively setup on the server:
- [Backups Cleanup](./roles/native-backups-cleanup/README.md) - Cleans up old backups
- [Btrfs Health Check](./roles/native-btrfs-health-check/README.md) - Checks the health of Btrfs file systems
- [Docker Health Check](./roles/native-docker-health-check/) - Checks the health of docker containers
- [Docker Reverse Proxy](./roles/native-docker-reverse-proxy/README.md) - Docker Reverse Proxy Solution
- [Docker Volume Backup](./roles/native-docker-volume-backup/) - Backup Solution for Docker Volumes
- [Pull Primary Backups](./roles/native-pull-primary-backups/README.md) - Pulls the backups from another server and stores them
- [Wireguard](./roles/native-wireguard/README.md) - Integrates the server in an wireguard vpn

## Server Administration

### Cleanup docker
``bash
docker stop $(docker ps -aq); docker rm $(docker ps -aq); docker volume rm $(docker volume ls -q);
``

### Restart

To mercifull restart the server and to prevent data lost type in: 

``bash
docker stop $(docker ps -a -q) && systemctl stop docker && shutdown -r +2 "The system will shutdown in 2 minutes"
``

May it's neccessary to restart some of the the docker containers manual afterwards. 

# Computer Playbook
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Ansible software to setup and administrate applications and docker images on Linux computers. 

With this tool you can setup all of the following application on bare metal servers and personal computers

## Bare Metal Servers

### Included Applications

#### Docker Applications

This software allows to setup the docker following applications:

- [Nextcloud](./roles/server_docker-nextcloud/README.md) - Cloud Software
- [Akaunting](./roles/server_docker-akaunting/README.md) - Business Controlling Software
- [Big Blue Button](./roles/server_docker-bigbluebutton/README.md) - Video Conference Software
- [Gitea](./roles/server_docker-gitea/README.md) - Version Controll Software
- [Joomla](./roles/server_docker-joomla/) - CMS Software
- [Mailu](./roles/server_docker-mailu/README.md) - Mailsoftware 
- [Peertube](./roles/server_docker-peertube/README.md) - Video Platform Software
- [pixelfed](./roles/server_docker-pixelfed/README.md) - Photo Platform Software
- [Wordpress](./roles/server_docker-wordpress/README.md) - Blog Software
- [YOURLS](./roles/server_docker-yourls/README.md) - URL Shortening Software
- [Mastodon](./roles/server_docker-mastodon/README.md) - Micro Blog Software
- [Media Wiki](./roles/server_docker-mediawiki/README.md) - Wiki Software
- [MyBB](./roles/server_docker-mybb/README.md) - Forum Software

#### Native Applications

This software shipts the following tools which are natively setup on the server:
- [Backups Cleanup](./roles/independent_backups-cleanup-timer/README.md) - Cleans up old backups
- [Btrfs Health Check](./roles/server_native-btrfs-health-check/README.md) - Checks the health of Btrfs file systems
- [Docker Health Check](./roles/server_native-docker-health-check/) - Checks the health of docker containers
- [Docker Reverse Proxy](./roles/server_native-docker-reverse-proxy/README.md) - Docker Reverse Proxy Solution
- [Docker Volume Backup](./roles/server_native-docker-volume-backup/) - Backup Solution for Docker Volumes
- [Pull Primary Backups](./roles/server_native-backups-consumer/README.md) - Pulls the backups from another server and stores them
- [Wireguard](./roles/server_native-wireguard/README.md) - Integrates the server in an wireguard vpn

### Server Administration

#### Cleanup docker
``bash
docker stop $(docker ps -aq); docker rm $(docker ps -aq); docker volume rm $(docker volume ls -q);
``

#### Restart

To mercifull restart the server and to prevent data lost type in: 

``bash
docker stop $(docker ps -a -q) && systemctl stop docker && shutdown -r +2 "The system will shutdown in 2 minutes"
``

May it's neccessary to restart some of the the docker containers manual afterwards. 


## Personal Computers

This playbooks offers the setup of Manjaro GNOME clients.

### Included Applications
- [Basic Linux Administration Tools](./roles/pc_collection-administrator-base/)
- [Network Analyzes Tools](./roles/pc_collection-administrator-network-analyze/)
- [Designer Tools](./roles/pc_collection-designer/)
- [Arduino Developer Tools](./roles/pc_collection-developer-arduino/)
- [Basic Developer Tools](./roles/pc_collection-developer-base/)
- [Bash Developer Tools](./roles/pc_collection-developer-bash/)
- [Java Developer Tools](./roles/pc_collection-developer-java/)
- [PHP Developer Tools](./roles/pc_collection-developer-php/)
- [Python Developer Tools](./roles/pc_collection-developer-python/)
- [Entertainment Software](./roles/pc_collection-entertainment/)
- [Games](./roles/pc_collection-games/)
- [Office Tools](./roles/pc_collection-office/)
- [Streaming Tools](./roles/pc_collection-streamer/)
- [Torrent Software](./roles/pc_collection-torrent/)
- ...

### Setup

Run:
```bash
ansible-galaxy collection install -r requirements.yml
```

## todo 
- implement: https://archlinux.org/packages/extra/x86_64/signal-desktop/

## See
- https://www.middlewareinventory.com/blog/run-ansible-playbook-locally/
- https://stackoverflow.com/questions/30533372/run-an-ansible-task-only-when-the-hostname-contains-a-string
- https://archived.forum.manjaro.org/t/running-android-applications-on-arch-using-anbox/53332
- https://www.reddit.com/r/ManjaroLinux/comments/cbkblb/guide_run_android_apps_on_manjaro_super_simple/ 

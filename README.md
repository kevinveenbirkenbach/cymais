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
- [Backups Cleanup](./roles/backups-cleanup-timer/README.md) - Cleans up old backups
- [Btrfs Health Check](./roles/btrfs-health-check/README.md) - Checks the health of Btrfs file systems
- [Docker Health Check](./roles/docker-health-check/) - Checks the health of docker containers
- [Docker Reverse Proxy](./roles/docker-reverse-proxy/README.md) - Docker Reverse Proxy Solution
- [Docker Volume Backup](./roles/docker-volume-backup/) - Backup Solution for Docker Volumes
- [Pull Primary Backups](./roles/backups-consumer/README.md) - Pulls the backups from another server and stores them
- [Wireguard](./roles/wireguard/README.md) - Integrates the server in an wireguard vpn

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

## todo 
- implement: https://archlinux.org/packages/extra/x86_64/signal-desktop/

## See
- https://www.middlewareinventory.com/blog/run-ansible-playbook-locally/
- https://stackoverflow.com/questions/30533372/run-an-ansible-task-only-when-the-hostname-contains-a-string
- https://archived.forum.manjaro.org/t/running-android-applications-on-arch-using-anbox/53332
- https://www.reddit.com/r/ManjaroLinux/comments/cbkblb/guide_run_android_apps_on_manjaro_super_simple/ 

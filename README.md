# Server-Playbook
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## Description
Ansible script to manage servers.

## Roles
The system use the following role namings:

| role prefix | meaning|
|---|---|
|system-|general system roles which apply basic configurations|
|native-|applications which run native on the system|
|docker-|applications which run on docker containers on the system|

## Debug

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

# Server-Manager
## Description
Ansible script to manage servers.

## Setup
To use this script execute:
``bash
ansible-galaxy install kewlfft.aur
``

## Update
``bash
ansible-playbook -i hosts site.yml
``

## Debug
### Cleanup docker
``bash
docker stop $(docker ps -aq); docker rm $(docker ps -aq); docker volume rm $(docker volume ls -q);
``

## topdo
- implement smtp
- implement administrator mail

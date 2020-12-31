# Server-Manager
## Description
Ansible script to manage servers.

## roles
The system use the following role namings:

| role prefix | meaning|
|---|---|
|system-|system changes|
|native-|applications which run native on the system|
|docker-|applications which run on docker containers on the system|

## Update
Follow the best [practices for inventories](https://docs.ansible.com/ansible/2.3/playbooks_best_practices.html) and execute ansible via:

``bash
ansible-playbook -i ~/your-inventories/inventorie/hosts site.yml
``

## Debug
### Cleanup docker
``bash
docker stop $(docker ps -aq); docker rm $(docker ps -aq); docker volume rm $(docker volume ls -q);
``

## todo
- implement smtp
- implement administrator mail

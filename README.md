# Server-Manager
## Description
Ansible script to manage servers.

## roles
The system use the following role namings:

| role prefix | meaning|
|---|---|
|system-|general system roles which apply basic configurations|
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
- Use docker-compose.yml files instead of the ansible inbuild docker-compose for more flexibility
- Implement https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-docker
- Refactor https://stackoverflow.com/questions/44784103/where-should-i-put-docker-compose-yml

## see
- https://wiki.archlinux.org/index.php/Ansible

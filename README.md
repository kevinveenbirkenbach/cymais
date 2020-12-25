# Server-Manager
## Description
Ansible script to manage servers.

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

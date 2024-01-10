#!/bin/python
#
# restart docker-compose configurations who have exited or unhealthy containers
#
import subprocess
import time
import os

errors = 0

def bash(command):
    print(command)
    process = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    stdout = out.splitlines()
    output = []
    for line in stdout:
        output.append(line.decode("utf-8"))
    if process.wait() > bool(0):
        print(command, out, err)
        raise Exception("Exitcode is greater then 0")
    return output

def list_to_string(list):
    return str(' '.join(list))

def print_bash(command):
    output = bash(command)
    print(list_to_string(output))
    return output

def find_docker_compose_file(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file == 'docker-compose.yml':
                return os.path.join(root, file)
    return None

waiting_time=600
blocker_running=True
while blocker_running:
    try: 
        bash("systemctl is-active --quiet backup-docker-to-local.cymais.service")
        bash("systemctl is-active --quiet update-docker.cymais.service")
        print("backup is running.")
        print("trying again in  " + str(waiting_time) + " seconds.")
        time.sleep(waiting_time)
    except:
        blocker_running=False
        print("No blocking service is running.")

unhealthy_container_names=print_bash('docker ps --filter health=unhealthy --format \'{{.Names}}\'')
exited_container_names=print_bash('docker ps --filter status=exited --format \'{{.Names}}\'')
failed_containers=unhealthy_container_names + exited_container_names

unfiltered_failed_docker_compose_repositories=[]
for failed_container in failed_containers:
    unfiltered_failed_docker_compose_repositories.append(failed_container.split('-')[0])

filtered_failed_docker_compose_repositories=list(dict.fromkeys(unfiltered_failed_docker_compose_repositories))

for filtered_failed_docker_compose_repository in filtered_failed_docker_compose_repositories:
    compose_file_path = find_docker_compose_file('/home/administrator/docker-compose/' + filtered_failed_docker_compose_repository)
    
    if compose_file_path:
        print("Restarting unhealthy container in:", compose_file_path)
        # Propably the cd is not necessary. But in rare cases it could be. To lazzy to test it now.
        print_bash(f'cd {os.path.dirname(compose_file_path)} && docker-compose -p "{filtered_failed_docker_compose_repository}" restart')
    else:
        print("Error: Docker Compose file not found for:", filtered_failed_docker_compose_repository)
        errors += 1

print("finished restart procedure.")
exit(errors)
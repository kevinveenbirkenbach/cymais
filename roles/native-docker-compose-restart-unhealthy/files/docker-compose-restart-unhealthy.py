#!/bin/python
#
# restart docker-compose configurations who have exited or unhealthy containers
#
import subprocess
import time

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

waiting_time=1800
backup_running=True
while backup_running:
    print("stop program for " + str(waiting_time) + "seconds.")
    time.sleep(waiting_time)
    try: 
        bash("systemctl is-active --quiet docker-volume-backup.service")
        print("backup is running.")
    except:
        backup_running=False
        print("no backup is running.")

unhealthy_container_names=print_bash('docker ps --filter health=unhealthy --format \'{{.Names}}\'')
exited_container_names=print_bash('docker ps --filter status=exited --format \'{{.Names}}\'')
failed_containers=unhealthy_container_names + exited_container_names

unfiltered_failed_docker_compose_repositories=[]
for failed_container in failed_containers:
    unfiltered_failed_docker_compose_repositories.append(failed_container.split('-')[0])

filtered_failed_docker_compose_repositories=list(dict.fromkeys(unfiltered_failed_docker_compose_repositories))
for filtered_failed_docker_compose_repository in filtered_failed_docker_compose_repositories:
    print("restarting unhealthy container: " + filtered_failed_docker_compose_repository)
    print_bash('cd /home/administrator/docker-compose/' + filtered_failed_docker_compose_repository + '/ && docker-compose restart')

print("finished restart procedure.")
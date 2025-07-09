#!/bin/python
#
# Restart Docker-Compose configurations with exited or unhealthy containers
#
import subprocess
import time
import os
import argparse

def bash(command):
    print(command)
    process = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    stdout = out.splitlines()
    stderr = err.decode("utf-8").strip()  # decode stderr
    output = [line.decode("utf-8") for line in stdout]
    if process.returncode > 0:
        print(command, out, err)
        raise Exception(stderr)  # pass the actual error text
    return output

def list_to_string(lst):
    return ' '.join(lst)

def print_bash(command):
    output = bash(command)
    print(list_to_string(output))
    return output

def find_docker_compose_file(directory):
    for root, _, files in os.walk(directory):
        if 'docker-compose.yml' in files:
            return os.path.join(root, 'docker-compose.yml')
    return None

def main(base_directory):
    errors = 0
    waiting_time = 600
    blocker_running = True
    
    while blocker_running:
        try: 
            bash("systemctl is-active --quiet bkp-docker-to-local.cymais.service")
            bash("systemctl is-active --quiet update-docker.cymais.service")
            print("Backup is running.")
            print(f"Trying again in {waiting_time} seconds.")
            time.sleep(waiting_time)
        except:
            blocker_running = False
            print("No blocking service is running.")
    
    unhealthy_container_names = print_bash("docker ps --filter health=unhealthy --format '{{.Names}}'")
    exited_container_names = print_bash("docker ps --filter status=exited --format '{{.Names}}'")
    failed_containers = unhealthy_container_names + exited_container_names
    
    unfiltered_failed_docker_compose_repositories = [container.split('-')[0] for container in failed_containers]
    filtered_failed_docker_compose_repositories = list(dict.fromkeys(unfiltered_failed_docker_compose_repositories))
    
    for repo in filtered_failed_docker_compose_repositories:
        compose_file_path = find_docker_compose_file(os.path.join(base_directory, repo))
        
        if compose_file_path:
            print("Restarting unhealthy container in:", compose_file_path)
            project_path = os.path.dirname(compose_file_path)
            try:
                print_bash(f'cd {project_path} && docker-compose -p "{repo}" restart')
            except Exception as e:
                if "port is already allocated" in str(e):
                    print("Detected port allocation problem. Executing recovery steps...")
                    print_bash(f'cd {project_path} && docker-compose down')
                    print_bash('systemctl restart docker')
                    print_bash(f'cd {project_path} && docker-compose -p "{repo}" up -d')
                else:
                    print("Unhandled exception during restart:", e)
                    errors += 1
        else:
            print("Error: Docker Compose file not found for:", repo)
            errors += 1

    
    print("Finished restart procedure.")
    exit(errors)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restart Docker-Compose configurations with exited or unhealthy containers.")
    parser.add_argument("base_directory", type=str, help="Base directory where Docker Compose configurations are located.")
    args = parser.parse_args()
    
    main(args.base_directory)
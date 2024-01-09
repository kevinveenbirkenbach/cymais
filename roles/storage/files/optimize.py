import subprocess
import os
import shutil

def run_command(command):
    """ Run a shell command and return its output """
    return subprocess.check_output(command, shell=True).decode('utf-8').strip()

# Path on the SSD where data will be moved
ssd_path = "/path/to/ssd"
hdd_path = "/path/to/hdd"

# List all Docker volumes
volumes = run_command("docker volume ls -q").splitlines()

def stop_containers(containers):
    """Stop a list of containers."""
    container_list = ' '.join(containers)
    print(f"Stopping containers {container_list}...")
    execute_shell_command(f"docker stop {container_list}")
    
def start_containers(containers):
    """Start a list of containers."""
    container_list = ' '.join(containers)
    print(f"Start containers {container_list}...")
    execute_shell_command(f"docker start {container_list}")

def is_database(image):
    return "postgres" in image or "mariadb" in image

def is_symbolic_link(file_path):
    return os.path.islink(file_path)

def get_volume_path(volume):
    return run_command(f"docker volume inspect --format '{{{{ .Mountpoint }}}}' {volume}")

def get_image(volume):
    return run_command(f"docker inspect --format='{{{{.Config.Image}}}}' {container}")

def pause_and_move(storage_path,volume):
    stop_containers(containers)
    # Create a new directory on the Storage
    storage_volume_path = os.path.join(storage_path, volume)
    os.makedirs(storage_volume_path, exist_ok=False)

    # Move the data
    for item in os.listdir(volume_path):
        shutil.move(os.path.join(volume_path, item), storage_volume_path)

    # Create a symbolic link
    os.symlink(storage_volume_path, volume_path)
    
    start_containers(containers)

for volume in volumes:
    # List all containers using this volume
    containers = run_command(f"docker ps -q --filter volume={volume}").splitlines()
    volume_path = get_volume_path(volume)
    if is_symbolic_link(volume_path):
        print(f"Skipped Volume {volume}. The storage path {volume_path} is a symbolic link.")
    
    for container in containers:
        # Get the image of the container
        image = get_image(container)

        # Check if the image contains "postgres" or "mariadb"
        if is_database(image):
            print(f"Container {container} with database image {image} found, using volume {volume}.")
            pause_and_move(ssd_path,volume)
        else:
            print(f"Container {container} with file image {image} found, using volume {volume}.")
            pause_and_move(hdd_path,volume)

print("Operation completed.")

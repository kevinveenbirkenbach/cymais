import subprocess
import os
import shutil
import argparse

def run_command(command):
    """ Run a shell command and return its output """
    return subprocess.check_output(command, shell=True).decode('utf-8').strip()

def stop_containers(containers):
    """Stop a list of containers."""
    container_list = ' '.join(containers)
    print(f"Stopping containers {container_list}...")
    run_command(f"docker stop {container_list}")

def start_containers(containers):
    """Start a list of containers."""
    container_list = ' '.join(containers)
    print(f"Starting containers {container_list}...")
    run_command(f"docker start {container_list}")

def is_database(image):
    return "postgres" in image or "mariadb" in image

def is_symbolic_link(file_path):
    return os.path.islink(file_path)

def get_volume_path(volume):
    return run_command(f"docker volume inspect --format '{{{{ .Mountpoint }}}}' {volume}")

def get_image(container):
    return run_command(f"docker inspect --format='{{{{.Config.Image}}}}' {container}")

def pause_and_move(storage_path, volume, volume_path, containers):
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

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Migrate Docker volumes to SSD or HDD based on container image.')
    parser.add_argument('--ssd_path', type=str, required=True, help='Path to the SSD storage')
    parser.add_argument('--hdd_path', type=str, required=True, help='Path to the HDD storage')
    
    # Parse arguments
    args = parser.parse_args()

    # Set paths from arguments
    ssd_path = args.ssd_path
    hdd_path = args.hdd_path

    # List all Docker volumes
    volumes = run_command("docker volume ls -q").splitlines()
    
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
                pause_and_move(ssd_path,volume,containers)
            else:
                print(f"Container {container} with file image {image} found, using volume {volume}.")
                pause_and_move(hdd_path,volume,containers)
    
    print("Operation completed.")
    
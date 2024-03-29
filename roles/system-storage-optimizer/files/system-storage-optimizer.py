import subprocess
import os
import time
import sys
import shutil
import argparse

def run_command(command):
    """ Run a shell command and return its output """
    print(command)
    output = subprocess.check_output(command, shell=True).decode('utf-8').strip()
    print(output)
    return output

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
    databases = {"postgres", "mariadb", "redis", "memcached", "mongo"}
    # Split the string at the colon and take the first part
    prefix = image.split(':')[0]
    # Check if the prefix is in the database names
    return prefix in databases

def is_symbolic_link(file_path):
    return os.path.islink(file_path)

def get_volume_path(volume):
    return run_command(f"docker volume inspect --format '{{{{ .Mountpoint }}}}' {volume}")

def get_image(container):
    return run_command(f"docker inspect --format='{{{{.Config.Image}}}}' {container}")

def run_rsync(src, dest):
    run_command(f"rsync -aP --remove-source-files {src} {dest}")

def delete_directory(path):
    """Deletes a directory and all its contents."""
    try:
        shutil.rmtree(path)
        print(f"Directory {path} was successfully deleted.")
    except OSError as e:
        print(f"Error deleting directory {path}: {e}")

def pause_and_move(storage_path, volume, volume_path, containers):
    stop_containers(containers)
    # Create a new directory on the Storage
    storage_volume_path = os.path.join(storage_path, 'data', 'docker', 'volumes', volume)
    os.makedirs(storage_volume_path,exist_ok=False)

    # Move the data
    run_rsync(f"{volume_path}/",f"{storage_volume_path}/")
    
    # Delete the source directory
    delete_directory(volume_path)

    # Create a symbolic link
    os.symlink(storage_volume_path, volume_path)
    
    start_containers(containers)

def has_container_with_database(containers):
    for container in containers:
        # Get the image of the container
        image = get_image(container)
        if is_database(image):
            return True
    return False
    

if __name__ == "__main__":
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Migrate Docker volumes to SSD or HDD based on container image.')
    parser.add_argument('--rapid-storage-path', type=str, required=True, help='Path to the SSD storage')
    parser.add_argument('--mass-storage-path', type=str, required=True, help='Path to the HDD storage')
    
    # Parse arguments
    args = parser.parse_args()

    # Set paths from arguments
    rapid_storage_path = args.rapid_storage_path
    mass_storage_path = args.mass_storage_path

    # List all Docker volumes
    volumes = run_command("docker volume ls -q").splitlines()
    
    for volume in volumes:
        volume_path = get_volume_path(volume)
        containers = run_command(f"docker ps -q --filter volume={volume}").splitlines()
        if not containers:
            print(f"Skipped Volume {volume}. It does not belong to a running container.")
        elif is_symbolic_link(volume_path):
            print(f"Skipped Volume {volume}. The storage path {volume_path} is a symbolic link.")
        elif has_container_with_database(containers):
            print(f"Safing volume {volume} on SSD.")
            pause_and_move(rapid_storage_path, volume, volume_path, containers)
        else:
            print(f"Safing volume {volume} on HDD.")
            pause_and_move(mass_storage_path, volume, volume_path, containers)

    print("Operation completed.")
    
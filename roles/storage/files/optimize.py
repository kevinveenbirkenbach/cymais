import subprocess
import os
import shutil

def run_command(command):
    """ Run a shell command and return its output """
    return subprocess.check_output(command, shell=True).decode('utf-8').strip()

# Path on the SSD where data will be moved
ssd_path = "/path/to/ssd"

# List all Docker volumes
volumes = run_command("docker volume ls -q").splitlines()

for volume in volumes:
    # List all containers using this volume
    containers = run_command(f"docker ps -q --filter volume={volume}").splitlines()

    for container in containers:
        # Get the image of the container
        image = run_command(f"docker inspect --format='{{{{.Config.Image}}}}' {container}")

        # Check if the image contains "postgres" or "mariadb"
        if "postgres" in image or "mariadb" in image:
            print(f"Container {container} with database image {image} found, using volume {volume}.")

            # Stop the container
            run_command(f"docker stop {container}")

            # Get the mount point of the volume
            volume_path = run_command(f"docker volume inspect --format '{{{{ .Mountpoint }}}}' {volume}")

            # Create a new directory on the SSD
            ssd_volume_path = os.path.join(ssd_path, volume)
            os.makedirs(ssd_volume_path, exist_ok=True)

            # Move the data
            for item in os.listdir(volume_path):
                shutil.move(os.path.join(volume_path, item), ssd_volume_path)

            # Create a symbolic link
            os.symlink(ssd_volume_path, volume_path)
        else:
            print(f"Container {container} with file image {image} found, using volume {volume}.")

print("Operation completed.")

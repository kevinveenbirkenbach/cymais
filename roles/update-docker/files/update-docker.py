import os
import subprocess
import sys
import time

def run_command(command):
    process = None
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = []

        for line in iter(process.stdout.readline, b''):
            decoded_line = line.decode()
            output.append(decoded_line)
            sys.stdout.write(decoded_line)

        return_code = process.wait()
        if return_code:
            full_output = ''.join(output)
            raise subprocess.CalledProcessError(return_code, command, output=full_output.encode())
    finally:
        if process and process.stdout:
            process.stdout.close()

def git_pull(directory):
    """
    Checks whether the Git repository in the specified directory is up to date and performs a git pull if necessary.

    Args:
        directory (str): The path to the directory of the Git repository.

    Returns:
        bool: True if a git pull was performed, otherwise False.
    """
    os.chdir(directory)
    print(f"Checking if the git repository in {directory} is up to date.")
    local = subprocess.check_output("git rev-parse @", shell=True).decode().strip()
    remote = subprocess.check_output("git rev-parse @{u}", shell=True).decode().strip()
    
    if local != remote:
        print("Repository is not up to date. Performing git pull.")
        run_command("git pull")
        return True;
    
    print("Repository is already up to date.")
    return False;
        
def get_image_digests(directory):
    compose_project = os.path.basename(directory)
    try:
        images_output = subprocess.check_output(
            f'docker images --format "{{{{.Repository}}}}:{{{{.Tag}}}}@{{{{.Digest}}}}" | grep {compose_project}', 
            shell=True
        ).decode().strip()
        return dict(line.split('@') for line in images_output.splitlines() if line)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:  # grep no match found
            return {}
        else:
            raise  # Other errors are still raised

def is_any_service_up(directory):
    os.chdir(directory)
    process = subprocess.Popen("docker-compose ps -q", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, _ = process.communicate()
    service_ids = output.decode().strip().splitlines()

    # Check if there are any service containers up
    if not service_ids:
        return False  # No services are up
    return True  # At least one service is up


def update_docker(directory):
    print(f"Checking for updates to Docker images in {directory}.")
    os.chdir(directory)
    before_digests = get_image_digests(directory)
    print("Pulling docker images.")
    
    need_to_build=False
    
    try:
        run_command("docker-compose pull")
    except subprocess.CalledProcessError as e:
        if "pull access denied" in e.output.decode() or "must be built from source" in e.output.decode():
            print("Need to build the image from source.")
            need_to_build=True
        else:
            print("Failed to pull images with unexpected error.")
            raise

    
    after_digests = get_image_digests(directory)
    if before_digests != after_digests:
        print("Changes detected in image digests. Rebuilding containers.")
        need_to_build=True
        
    if need_to_build:
        run_command("docker-compose build")
        start_docker(directory)
    else:
        print("Docker images are up to date. No rebuild necessary.")

def update_nextcloud():
    print("Start Nextcloud update procedure.")
    update_procedure("docker-compose exec -T -u www-data application /var/www/html/occ upgrade")
    update_procedure("docker-compose exec -T -u www-data application /var/www/html/occ maintenance:repair")
    update_procedure("docker-compose exec -T -u www-data application /var/www/html/occ app:update --all")
    update_procedure("docker-compose exec -T -u www-data application /var/www/html/occ maintenance:mode --off")
    
def update_discourse(directory):
    os.chdir(directory)
    print("Start Discourse update procedure.")
    update_procedure("./launcher rebuild app")
    
# This procedure waits until the container is up
def update_procedure(command):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            run_command(command)
            break  # If the command succeeds, exit the loop
        except subprocess.CalledProcessError as e:
            if attempt < max_attempts - 1:  # Check if it's not the last attempt
                print(f"Attempt {attempt + 1} failed, retrying in 60 seconds...")
                time.sleep(60)  # Wait for 60 seconds before retrying
            else:
                print("All attempts to update Nextcloud apps have failed.")
                raise  # Re-raise the last exception after all attempts fail


def start_docker(directory):
    if is_any_service_up(directory):
        print(f"Restarting containers in {directory}.")
        run_command("docker-compose up -d --force-recreate")
    else:
        print(f"Skipped starting. No service is up in {directory}.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the parent directory as a parameter.")
        sys.exit(1)

    parent_directory = sys.argv[1]
    for dir_entry in os.scandir(parent_directory):
        if dir_entry.is_dir():
            dir_path = dir_entry.path
            print(f"Checking for updates in: {dir_path}")
            
            if os.path.isdir(os.path.join(dir_path, ".git")):
                git_repository_was_pulled = git_pull(dir_path)
            
            # Discourse is an exception and uses own update command instead of docker compose
            if os.path.basename(dir_path) == "discourse":
                if git_repository_was_pulled:
                    update_discourse(dir_path)
                else:
                    print("Discourse update skipped. No changes in git repository.")
            else:
                update_docker(dir_path)
                # Nextcloud needs additional update procedures
                if os.path.basename(dir_path) == "nextcloud":
                    update_nextcloud()

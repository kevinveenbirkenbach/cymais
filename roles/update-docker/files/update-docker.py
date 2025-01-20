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

def git_pull():
    """
    Checks whether the Git repository in the specified directory is up to date and performs a git pull if necessary.
    """
    print(f"Checking if the git repository is up to date.")
    local = subprocess.check_output("git rev-parse @", shell=True).decode().strip()
    remote = subprocess.check_output("git rev-parse @{u}", shell=True).decode().strip()
    
    if local != remote:
        print("Repository is not up to date. Performing git pull.")
        run_command("git pull")
        return True
    
    print("Repository is already up to date.")
    return False
        
def get_image_digests(directory):
    """
    Retrieves the image digests for all images in the specified Docker Compose project.
    """
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

def is_any_service_up():
    """
    Checks if any Docker services are currently running.
    """
    process = subprocess.Popen("docker-compose ps -q", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, _ = process.communicate()
    service_ids = output.decode().strip().splitlines()
    return bool(service_ids)

def pull_docker_images():
    """
    Pulls the latest Docker images for the project.
    """
    print("Pulling docker images.")
    try:
        run_command("docker-compose pull")
    except subprocess.CalledProcessError as e:
        if "pull access denied" in e.output.decode() or "must be built from source" in e.output.decode():
            print("Need to build the image from source.")
            return True
        else:
            print("Failed to pull images with unexpected error.")
            raise
    return False

def update_docker(directory):
    """
    Checks for updates to Docker images and rebuilds containers if necessary.
    """
    print(f"Checking for updates to Docker images in {directory}.")        
    before_digests = get_image_digests(directory)
    need_to_build = pull_docker_images()
    after_digests = get_image_digests(directory)
    if before_digests != after_digests:
        print("Changes detected in image digests. Rebuilding containers.")
        need_to_build = True
        
    if need_to_build:
        run_command("docker-compose build")
        start_docker(directory)
    else:
        print("Docker images are up to date. No rebuild necessary.")

def update_mastodon():
    """
    Runs the database migration for Mastodon to ensure all required tables are up to date.
    """
    print("Starting Mastodon database migration.")
    run_command("docker compose exec -T web bash -c 'RAILS_ENV=production bin/rails db:migrate'")
    print("Mastodon database migration complete.")

def upgrade_listmonk():
    """
    Runs the upgrade for Listmonk
    """
    print("Starting Listmonk upgrade.")
    run_command('echo "y" | docker compose run -T application ./listmonk --upgrade')
    print("Upgrade complete.")

def update_nextcloud():
    """
    Performs the necessary Nextcloud update procedures, including maintenance and app updates.
    """
    print("Start Nextcloud upgrade procedure.")
    update_procedure("docker-compose exec -T -u www-data application /var/www/html/occ upgrade")
    print("Start Nextcloud repairing procedure.")
    update_procedure("docker-compose exec -T -u www-data application /var/www/html/occ maintenance:repair --include-expensive")
    print("Start Nextcloud update procedure.")
    update_procedure("docker-compose exec -T -u www-data application /var/www/html/occ app:update --all")
    print("Start Nextcloud add-missing procedure.")
    update_procedure("docker-compose exec -T -u www-data application /var/www/html/occ db:add-missing-columns")
    update_procedure("docker-compose exec -T -u www-data application /var/www/html/occ db:add-missing-indices")
    update_procedure("docker-compose exec -T -u www-data application /var/www/html/occ db:add-missing-primary-keys")
    print("Deacitvate Maintanance Mode")
    update_procedure("docker-compose exec -T -u www-data application /var/www/html/occ maintenance:mode --off")
    
def update_discourse(directory):
    """
    Updates Discourse by running the rebuild command on the launcher script.
    """
    os.chdir(directory)
    print("Start Discourse update procedure.")
    update_procedure("./launcher rebuild app")

def update_procedure(command):
    """
    Attempts to execute a command up to a maximum number of retries.
    """
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
                print("All attempts to update have failed.")
                raise  # Re-raise the last exception after all attempts fail

def start_docker(directory):
    """
    Starts or restarts Docker services in the specified directory.
    """
    if is_any_service_up():
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
            os.chdir(dir_path)
            
            if os.path.isdir(os.path.join(dir_path, ".git")):
                git_repository_was_pulled = git_pull()
            
            # Discourse is an exception and uses own update command instead of docker compose
            if os.path.basename(dir_path) == "discourse":
                if git_repository_was_pulled:
                    update_discourse(dir_path)
                else:
                    print("Discourse update skipped. No changes in git repository.")
            elif os.path.basename(dir_path) == "matrix":
                # No autoupdate for matrix is possible atm, 
                # due to the reason that the role has to be executed every time.
                # The update has to be executed in the role
                # @todo implement in future
                pass
            else:
                # Pull and update docker images
                update_docker(dir_path)
                
                # The following instances need additional update and upgrade procedures
                if os.path.basename(dir_path) == "nextcloud":
                    update_nextcloud()
                elif os.path.basename(dir_path) == "listmonk":
                    upgrade_listmonk()
                elif os.path.basename(dir_path) == "mastodon":
                    update_mastodon()

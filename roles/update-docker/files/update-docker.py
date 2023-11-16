import os
import subprocess
import sys

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = []

    # Iterate over the output lines
    for line in iter(process.stdout.readline, b''):
        decoded_line = line.decode()
        output.append(decoded_line)
        sys.stdout.write(decoded_line)

    process.stdout.close()
    return_code = process.wait()
    if return_code:
        # Join the output list to create a single string
        full_output = ''.join(output)
        raise subprocess.CalledProcessError(return_code, command, output=full_output.encode())


def git_pull(directory):
    os.chdir(directory)
    print(f"Checking if the git repository in {directory} is up to date.")
    local = subprocess.check_output("git rev-parse @", shell=True).decode().strip()
    remote = subprocess.check_output("git rev-parse @{u}", shell=True).decode().strip()
    
    if local != remote:
        print("Repository is not up to date. Performing git pull.")
        run_command("git pull")
    else:
        print("Repository is already up to date.")
        
def get_image_digests(directory):
    compose_project = os.path.basename(directory)
    images_output = subprocess.check_output(
        f'docker images --format "{{{{.Repository}}}}:{{{{.Tag}}}}@{{{{.Digest}}}}" | grep {compose_project}', 
        shell=True
    ).decode().strip()
    return dict(line.split('@') for line in images_output.splitlines() if line)

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
    if before_digests != after_digest:
        print("Changes detected in image digests. Rebuilding containers.")
        need_to_build=True
        
    if need_to_build:
        run_command("docker-compose up -d --build --force-recreate")
    else:
        print("Docker images are up to date. No rebuild necessary.")

def update_nextcloud(directory):
    print("Updating Nextcloud apps.")
    run_command("docker-compose exec -T -u www-data application /var/www/html/occ app:update --all")

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
                git_pull(dir_path)
            
            update_docker(dir_path)
            
            if os.path.basename(dir_path) == "nextcloud":
                update_nextcloud(dir_path)

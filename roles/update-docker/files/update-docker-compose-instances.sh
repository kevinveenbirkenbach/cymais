#!/bin/bash

# Check if a path argument was provided
if [ -z "$1" ]; then
  echo "Please provide the path to the parent directory as a parameter."
  exit 1
fi

# Iterate over all directories in the parent directory
for dir in "$1"/*; do
  # Check if it is indeed a directory
  if [ -d "$dir" ]; then
    echo "Checking for updates in: $dir"
    cd "$dir"
    
    # Check if directory is a Git repository
    if [ -d ".git" ]; then
      echo "Checking if the git repository is up to date."
      git fetch
      LOCAL=$(git rev-parse @)
      REMOTE=$(git rev-parse @{u})
      
      # If local commit differs from remote, pull the changes
      if [ "$LOCAL" != "$REMOTE" ]; then
        echo "Repository is not up to date. Performing git pull."
        git pull || exit 3
      else
        echo "Repository is already up to date."
      fi
    fi

    # Pull the latest images and rebuild the containers
    echo "Pulling docker images and rebuilding containers."
    docker-compose pull && docker-compose up -d --build --force-recreate || exit 1
    
    # Additional command for the 'nextcloud' directory
    if [ "$(basename "$dir")" == "nextcloud" ]; then
      echo "Updating Nextcloud apps."
      docker-compose exec -T -u www-data application /var/www/html/occ app:update --all || exit 2
    fi
    cd - > /dev/null
  fi
done

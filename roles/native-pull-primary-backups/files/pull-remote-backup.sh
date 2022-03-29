#!/bin/bash
# @param $1 hostname from which backup should be pulled

# error counter
errors=0

source_host="backup@$1"
source_machine_id="$( (ssh "$source_host" sha256sum /etc/machine-id) | head -c 64)" || exit 1
source_path="/Backups/$source_machine_id/"
directories="$(ssh "$source_host" find "$source_path" -maxdepth 1 -type d)" || exit 1

for backup_type_dir in $directories; do
  if [ "$backup_type_dir" != "$source_path" ]; then
    # this folder is neccessary to make restricted rsync possible:
    current_version="$backup_type_dir/versions/current/"
    # this is the folder where the versions will be copied to:
    diff_store="$backup_type_dir/versions/$(date '+%Y%m%d%H%M%S')/"
    # this is the folder which contains the actual backup:
    latest_path="$backup_type_dir/latest/"
    # source path of the backup files:
    remote_source_path="$source_host:$latest_path"
    # file in which the logs will be saved:
    log_path="$backup_type_dir/log.txt"

    # create working folders:
    mkdir -vp "$latest_path"
    mkdir -vp "$diff_store"
    rm -vr "$current_version"
    mkdir -vp "$current_version"

    # do backup:
    rsync -abP --delete --delete-excluded --rsync-path="sudo rsync" --log-file="$log_path" --backup-dir="$current_version" "$remote_source_path" "$latest_path" || ((errors+=1));
    mv -v "$current_version"* "$diff_store"
  fi
done
exit $errors;

#!/bin/bash
# @param $1 hostname from which backup should be pulled

# error counter
errors=0

source_host="backup@$1"
source_machine_id="$( (ssh "$source_host" sha256sum /etc/machine-id) | head -c 64)" || exit 1
source_path="/Backups/$source_machine_id/"
directories="$(ssh "$source_host" find "$source_path" -maxdepth 1 -type d)" || exit 1

for folder in $directories; do
  if [ "$folder" != "$source_path" ]; then
    # this folder is neccessary to make restricted rsync possible:
    diff_current="$folder/diffs/current/"
    # this is the folder where the diffs will be copied to:
    diff_store="$folder/diffs/$(date '+%Y%m%d%H%M%S')/"
    # this is the folder which contains the actual backup:
    latest_path="$folder/latest/"
    # source path of the backup files:
    remote_source_path="$source_host:$latest_path"
    # file in which the logs will be saved:
    log_path="$folder/log.txt"

    # create working folders:
    mkdir -vp "$latest_path"
    mkdir -vp "$diff_store"
    rm -vr "$diff_current"
    mkdir -vp "$diff_current"

    # do backup:
    rsync -abP --delete --delete-excluded --rsync-path="sudo rsync" --log-file="$log_path" --backup-dir="$diff_current" "$remote_source_path" "$latest_path" || ((errors+=1));
    mv -v "$diff_current"* "$diff_store"
  fi
done
exit $errors;

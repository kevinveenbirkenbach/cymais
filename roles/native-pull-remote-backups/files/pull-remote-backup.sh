#!/bin/bash
# @param $1 hostname from which backup should be pulled
source_host="backup@$1"
source_machine_id="$( (ssh "$source_host" sha256sum /etc/machine-id) | head -c 64)"
source_path="/Backups/$source_machine_id/"
directories="$(ssh "$source_host" find "$source_path" -maxdepth 1 -type d)"
for folder in $directories; do
  if [ "$folder" != "$source_path" ]; then
    diff_path="$folder/diffs/$(date '+%Y%m%d%H%M%S')/"
    latest_path="$folder/latest/"
    remote_source_path="$source_host:$latest_path"
    log_path="$folder/log.txt"
    mkdir -vp "$latest_path"
    mkdir -vp "$diff_path"
    rsync -abvv --delete --delete-excluded --rsync-path="sudo rsync" --log-file="$log_path" --backup-dir="$diff_path" "$remote_source_path" "$latest_path" || exit 1
  fi
done

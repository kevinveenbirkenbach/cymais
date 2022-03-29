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
    # folder which contains versions
    versions_dir="$backup_type_dir/versions/"
    # link name of last backup
    latest_version_link="$backup_type_dir/latest"
    # this folder contains the last backup
    latest_version_dir="$versions_dir$(date '+%Y%m%d%H%M%S')/"
    # this is the link name of the previous version
    previous_version_link="$backup_type_dir/previous"
    # source path of the backup files:
    remote_source_path="$source_host:$latest_version_link/"

    #identifiy previous version
    versions=( $(basename -a "$versions_dir"*/ | sort) )|| exit 1
    last_version="${versions[-1]}" || exit 1
    previous_version_dir="$versions_dir$last_version/"

    # create working folders:
    mkdir -vp "$latest_version_dir"

    # delete links
    rm -v "$latest_version_link"
    rm -v "$previous_version_link"

    # create links
    ln -vs "$latest_version_dir" "$latest_version_link" || exit 1
    ln -vs "$previous_version_dir" "$previous_version_link"|| exit 1

    # do backup:
    rsync -abP --delete --delete-excluded --rsync-path="sudo rsync" --link-dest="$previous_version_link" "$remote_source_path" "$latest_version_link" || ((errors+=1));
  fi
done
exit $errors;

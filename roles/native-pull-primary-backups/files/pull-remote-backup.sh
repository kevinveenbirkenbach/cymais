#!/bin/bash
# @param $1 hostname from which backup should be pulled

# error counter
errors=0

remote_host="backup@$1"
remote_machine_id="$( (ssh "$remote_host" sha256sum /etc/machine-id) | head -c 64 )" || exit 1
general_backup_machine_dir="/Backups/$remote_machine_id/"
remote_backup_types="$(ssh "$remote_host" find "$general_backup_machine_dir" -maxdepth 1 -type d -execdir basename {} ';')" || exit 1

for backup_type in $remote_backup_types; do
  if [ "$backup_type" != "$remote_machine_id" ]; then
    general_backup_type_dir="$general_backup_machine_dir""$backup_type/"
    # folder which contains versions
    general_versions_dir="$general_backup_type_dir""versions/"
    # link name of last backup
    general_latest_version_link="$general_backup_type_dir""latest"
    
    # this folder contains the last backup
    local_latest_version_dir="$general_versions_dir$(date '+%Y%m%d%H%M%S')/"
    # this is the link name of the previous version
    local_previous_version_link="$general_backup_type_dir""previous"

    #identifiy previous version
    local_versions=( $(basename -a "$general_versions_dir"*/ | sort) )|| exit 1
    local_last_version="${local_versions[-1]}" || exit 1
    local_previous_version_dir="$general_versions_dir""$last_version/"

    # source path of the backup files:
    remote_last_version_dir="$(readlink -f $general_latest_version_link)"
    remote_source_path="$remote_host:$remote_last_version_dir/"

    # create working folders:
    mkdir -vp "$local_latest_version_dir"

    # delete links
    rm -v "$general_latest_version_link"
    rm -v "$local_previous_version_link"

    # create links
    ln -vs "$local_latest_version_dir" "$general_latest_version_link" || exit 1
    ln -vs "$local_previous_version_dir" "$local_previous_version_link"|| exit 1

    # do backup:
    rsync -abP --delete --delete-excluded --rsync-path="sudo rsync" --link-dest="$local_previous_version_link" "$remote_source_path" "$general_latest_version_link" || ((errors+=1));
  fi
done
exit $errors;

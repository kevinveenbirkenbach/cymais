#!/bin/sh

# log command
if [ -n "$SSH_ORIGINAL_COMMAND" ]
then
  echo "`/bin/date`: $SSH_ORIGINAL_COMMAND" | systemd-cat -t "ssh-wrapper.sh"
fi

# define executable commands
get_hashed_machine_id="sha256sum /etc/machine-id";
hashed_machine_id="$($get_hashed_machine_id | head -c 64)"
get_backup_types="find /Backups/$hashed_machine_id/ -maxdepth 1 -type d -execdir basename {} ;";


# @todo This configuration is not scalable yet. If other backup services then backup-docker-to-local are integrated, this logic needs to be optimized
get_version_directories="ls -d /Backups/$hashed_machine_id/backup-docker-to-local/*"
last_version_directory="$($get_version_directories | tail -1)"
rsync_command="sudo rsync --server --sender -blogDtpre.iLsfxCIvu . $last_version_directory/"

# filter commands
case "$SSH_ORIGINAL_COMMAND" in
	"$get_hashed_machine_id")
		$get_hashed_machine_id
		;;
	"$get_version_directories")
		$get_version_directories
		;;
	"$get_backup_types")
		$get_backup_types
		;;
	"$rsync_command")
		$rsync_command
		;;
	*)
		echo "This command is not supported."
		exit 1
		;;
esac

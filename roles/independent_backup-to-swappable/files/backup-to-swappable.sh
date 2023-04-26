#! /bin/sh
backup_to_swappable_destination_path="$1" &&
echo "backup to swappable destination path: $backup_to_swappable_destination_path" &&

source_path="$2" &&
echo "source path: $source_path" || exit 1

if [ ! -d "$backup_to_swappable_destination_path" ]; then
    echo "Directory $backup_to_swappable_destination_path does not exist" &&
    exit 1
fi

machine_id="$(sha256sum /etc/machine-id | head -c 64 )" &&
echo "machine id: $machine_id" &&

versions_path="$backup_to_swappable_destination_path$machine_id/backup-to-swappable/" &&
echo "versions path: $versions_path" || exit 1

if [ ! -d "$versions_path" ]; then
    echo "Creating $versions_path..." &&
    mkdir -vp $versions_path || exit 1
fi 

previous_version_path="$(ls -d $versions_path* | tail -1)" &&
echo "previous versions path: $previous_version_path" &&

current_version_path="$versions_path$(date '+%Y%m%d%H%M%S')" &&
echo "current versions path: $current_version_path" &&

echo "creating backup destination folder..." &&
mkdir -vp "$current_version_path" &&

echo "Starting syncronization..."
rsync -abP --delete --delete-excluded --link-dest="$previous_version_path" "$source_path" "$current_version_path" &&
echo "Syncronization finished." || exit 1
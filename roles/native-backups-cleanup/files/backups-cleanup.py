# @see https://stackoverflow.com/questions/48929553/get-hard-disk-size-in-python
import psutil
import shutil
import os
backup_disk_path = "/media/encrypteddrive-sda/"
backups_folder_path = os.path.join(backup_disk_path, "Backups/")

while psutil.disk_usage(backup_disk_path).percent > 50:
    print("%d %% of disk %s are used. Freeing space..." % (psutil.disk_usage(backup_disk_path).percent,backup_disk_path))
    for primary_directory in os.listdir(backups_folder_path):
        primary_directory = os.path.join(backups_folder_path, primary_directory)
        for application_directory in os.listdir(primary_directory):
            application_directory = os.path.join(primary_directory, application_directory)
            diffs_directory = os.path.join(application_directory, "diffs/")
            diffs = os.listdir(diffs_directory)
            diffs.sort(reverse=False)
            delete_diff = diffs_directory + diffs[0]
            print("Deleting %s..." % (delete_diff))
            shutil.rmtree(delete_diff)
print("Cleaning up finished: %d %% of disk %s are used." % (psutil.disk_usage(backup_disk_path).percent,backup_disk_path))

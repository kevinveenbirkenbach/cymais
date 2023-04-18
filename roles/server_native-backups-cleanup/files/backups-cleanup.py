import psutil
import shutil
import os
import argparse

# Validating arguments
parser = argparse.ArgumentParser()
parser.add_argument('--maximum-backup-size-percent', type=int, dest='maximum_backup_size_percent',required=True, choices=range(0,100), help="The directory from which the data should be encrypted.")
parser.add_argument('--backups-folder-path',type=str,dest='backups_folder_path',required=True, help="The folder in which the backups are stored")
args = parser.parse_args()

deleted = True
while psutil.disk_usage(args.backups_folder_path).percent > args.maximum_backup_size_percent and deleted:
    deleted = False
    print("%d %% of disk %s are used. Freeing space..." % (psutil.disk_usage(args.backups_folder_path).percent,args.backups_folder_path))
    for primary_directory in os.listdir(args.backups_folder_path):
        primary_directory = os.path.join(args.backups_folder_path, primary_directory)
        for application_directory in os.listdir(primary_directory):
            application_directory = os.path.join(primary_directory, application_directory)
            versions_directory = os.path.join(application_directory, "versions/")
            versions = os.listdir(versions_directory)
            versions.sort(reverse=False)
            if len(versions) >= 1:
                delete_diff = versions_directory + versions[0]
                print("Deleting %s..." % (delete_diff))
                shutil.rmtree(delete_diff)
                deleted = True
if not deleted:
    print("All versions had been deleted!")
print("Cleaning up finished: %d %% of disk %s are used." % (psutil.disk_usage(args.backups_folder_path).percent,args.backups_folder_path))

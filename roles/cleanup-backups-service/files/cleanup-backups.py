import psutil
import shutil
import os
import argparse
import subprocess

# Validating arguments
parser = argparse.ArgumentParser()
parser.add_argument('--maximum-backup-size-percent', type=int, dest='maximum_backup_size_percent',required=True, choices=range(0,100), help="The directory from which the data should be encrypted.")
parser.add_argument('--backups-folder-path',type=str,dest='backups_folder_path',required=True, help="The folder in which the backups are stored")
args = parser.parse_args()

def print_used_disc_space(backups_folder_path):
    print("%d %% of disk %s are used" % (psutil.disk_usage(backups_folder_path).percent,backups_folder_path))  

def is_directory_used_by_another_process(directory_path):
    command= "lsof " + directory_path
    process = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    # @See https://stackoverflow.com/questions/29841984/non-zero-exit-code-for-lsof
    if process.wait() > bool(0):
        return False
    return True

def isSmallerThenMaximumBackupSize(maximum_backup_size_percent,backups_folder_path):
    current_disc_usage_percent=psutil.disk_usage(backups_folder_path).percent
    return current_disc_usage_percent > maximum_backup_size_percent

def isDirectoryDeletable(version, versions_directory, version_path):
    print("Checking directory %s ..." % (version_path))
    if version == versions[-1]:
        print("Directory %s contains the last version of the backup. Skipped." % (version_path))
        return False
    
    if is_directory_used_by_another_process(version_path):
        print("Directory %s is used by another process. Skipped." % (version_path))
        return False
     
backups_folder_path=args.backups_folder_path
for host_backup_directory_name in os.listdir(backups_folder_path):
    host_backup_directory_path = os.path.join(backups_folder_path, host_backup_directory_name)
    for application_directory in os.listdir(host_backup_directory_path):
        
        # The directory which contains all backup versions of the application
        versions_directory = os.path.join(host_backup_directory_path, application_directory) + "/"
                    
        versions = os.listdir(versions_directory)
        versions.sort(reverse=False)
        
        print_used_disc_space(backups_folder_path)  
        for version in versions:
            version_path=os.path.join(versions_directory, version)
            if not isDirectoryDeletable(version, versions_directory, version_path):
                continue

            if isSmallerThenMaximumBackupSize(maximum_backup_size_percent,backups_folder_path):
                print("Deleting %s to free space." % (version_path))
                shutil.rmtree(version_path)
                new_disc_usage_percent=psutil.disk_usage(backups_folder_path).percent
                difference_percent=old_disc_usage_percent-new_disc_usage_percent
                print("{:6.2f} %% of drive freed".format(difference_percent))
                continue
            
print_used_disc_space(backups_folder_path)            
print("Cleaning up finished.")
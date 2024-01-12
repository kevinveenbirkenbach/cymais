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
    
def deleteVersion(version_path, backups_folder_path):
    print("Deleting %s to free space." % (version_path))
    shutil.rmtree(version_path)
    new_disc_usage_percent=psutil.disk_usage(backups_folder_path).percent
    difference_percent=old_disc_usage_percent-new_disc_usage_percent
    print("{:6.2f} %% of drive freed".format(difference_percent))

def count_total_application_directories(backups_folder_path):
    total_app_directories = 0
    for host_backup_directory_name in os.listdir(backups_folder_path):
        host_backup_directory_path = os.path.join(backups_folder_path, host_backup_directory_name)
        total_app_directories += sum(os.path.isdir(os.path.join(host_backup_directory_path, d)) for d in os.listdir(host_backup_directory_path))
    return total_app_directories

def count_total_version_folders(backups_folder_path):
    total_version_folders = 0
    for host_backup_directory_name in os.listdir(backups_folder_path):
        host_backup_directory_path = os.path.join(backups_folder_path, host_backup_directory_name)
        for application_directory in os.listdir(host_backup_directory_path):
            versions_directory = os.path.join(host_backup_directory_path, application_directory)
            total_version_folders += sum(os.path.isdir(os.path.join(versions_directory, d)) for d in os.listdir(versions_directory))
    return total_version_folders

def average_version_directories_per_application(backups_folder_path,blur=-1):
    total_app_directories = count_total_application_directories(backups_folder_path)
    total_version_folders = count_total_version_folders(backups_folder_path)
    
    if total_app_directories == 0:
        return 0

    average = total_version_folders / total_app_directories
    return int(average) - blur

def getAmountOfIterration(versions,average_version_directories_per_application):
    return len(versions) - average_version_directories_per_application

def deletInterration(backups_folder_path,average_version_directories_per_application):
    for host_backup_directory_name in os.listdir(backups_folder_path):
        host_backup_directory_path = os.path.join(backups_folder_path, host_backup_directory_name)
        for application_directory in os.listdir(host_backup_directory_path):
            
            # The directory which contains all backup versions of the application
            versions_directory = os.path.join(host_backup_directory_path, application_directory) + "/"
                        
            versions = os.listdir(versions_directory)
            versions.sort(reverse=False)
            version_iterration=0 
            while version_iterration < getAmountOfIterration(versions,average_version_directories_per_application):
                print_used_disc_space(backups_folder_path)
                version = versions[version_iterration]
                version_path=os.path.join(versions_directory, version)
                if isDirectoryDeletable(version, versions_directory, version_path):
                    deleteVersion(version_path, backups_folder_path)
                version_iterration += 1 
                     
backups_folder_path=args.backups_folder_path
maximum_backup_size_percent=args.maximum_backup_size_percent

itteration_counter = 1
while isSmallerThenMaximumBackupSize(maximum_backup_size_percent, backups_folder_path):
    if itteration_counter > 200:
        raise Exception("Iteration limit exceeded")

    print(f"Delete Iteration: {itteration_counter}")
    average_version_directories = average_version_directories_per_application(backups_folder_path)
    print(f"Average version directories per application directory: {average_version_directories}")
    deleteIteration(backups_folder_path, average_version_directories)    
    itteration_counter += 1

print_used_disc_space(backups_folder_path)            
print("Cleaning up finished.")
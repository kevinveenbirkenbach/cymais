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

def print_used_disc_space():
    print("%d %% of disk %s are used" % (psutil.disk_usage(args.backups_folder_path).percent,args.backups_folder_path))  

def is_directory_used_by_another_process(directory_path):
    command= "lsof " + directory_path
    process = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error:
        raise Exception(error.strip())
    if output:
        return True
    return False

for host_backup_directory_name in os.listdir(args.backups_folder_path):
    host_backup_directory_path = os.path.join(args.backups_folder_path, host_backup_directory_name)
    for application_directory in os.listdir(host_backup_directory_path):
        
        # The directory which contains all backup versions of the application
        versions_directory = os.path.join(host_backup_directory_path, application_directory) + "/"
                    
        versions = os.listdir(versions_directory)
        versions.sort(reverse=False)
        
        print_used_disc_space()  
        for version in versions:
            version_path=os.path.join(versions_directory, version)
            version_status_pulling_path=os.path.join(versions_directory, version, ".pulling")
            print("Checking directory %s ..." % (version_path))
            if version == versions[-1]:
                print("Directory %s contains the last version of the backup. Skipped." % (version_path))
                continue
            
            if is_directory_used_by_another_process(version_path):
                print("Directory %s is used by another process. Skipped." % (version_path))
                continue
             
            if psutil.disk_usage(args.backups_folder_path).percent > args.maximum_backup_size_percent:
                print("Deleting %s to free space." % (version_path))
                shutil.rmtree(version_path)
                continue
            
            if os.path.exists(version_status_pulling_path):
                print("Deleting %s due to unfinished pull." % (version_path))
                shutil.rmtree(version_path)
                continue
            
print_used_disc_space()            
print("Cleaning up finished.")
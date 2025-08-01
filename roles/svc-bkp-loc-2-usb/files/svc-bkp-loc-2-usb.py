#!/usr/bin/env python3

import sys
import subprocess
import shutil
import os
import glob
import datetime

def main():
    source_path = sys.argv[1]
    print(f"source path: {source_path}")
    
    backup_to_usb_destination_path = sys.argv[2]
    print(f"backup to usb destination path: {backup_to_usb_destination_path}")
    
    if not os.path.isdir(backup_to_usb_destination_path):
        print(f"Directory {backup_to_usb_destination_path} does not exist")
        sys.exit(1)
    
    machine_id = subprocess.run(["sha256sum", "/etc/machine-id"], capture_output=True, text=True).stdout.strip()[:64]
    print(f"machine id: {machine_id}")
    
    versions_path = os.path.join(backup_to_usb_destination_path, f"{machine_id}/svc-bkp-loc-2-usb/")
    print(f"versions path: {versions_path}")
    
    if not os.path.isdir(versions_path):
        print(f"Creating {versions_path}...")
        os.makedirs(versions_path, exist_ok=True)
    
    previous_version_path = max(glob.glob(f"{versions_path}*"), key=os.path.getmtime, default=None)
    print(f"previous versions path: {previous_version_path}")
    
    current_version_path = os.path.join(versions_path, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    print(f"current versions path: {current_version_path}")
    
    print("Creating backup destination folder...")
    os.makedirs(current_version_path, exist_ok=True)
    
    print("Starting synchronization...")
    try:
        rsync_command = [
            "rsync", "-abP", "--delete", "--delete-excluded"
        ]
        if previous_version_path is not None:
            rsync_command.append("--link-dest=" + previous_version_path)
        rsync_command.extend([source_path, current_version_path])
        rsync_output = subprocess.check_output(rsync_command, stderr=subprocess.STDOUT, text=True)
        
        print(rsync_output)
        print("Synchronization finished")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(e.output)
        if "rsync warning: some files vanished before they could be transferred" in e.output:
            print("Synchronization finished with rsync warning")
            sys.exit(0)
        else:
            print("Synchronization failed")
            sys.exit(1)

if __name__ == "__main__":
    main()
# @see https://stackoverflow.com/questions/48929553/get-hard-disk-size-in-python
# import shutil
import psutil
import os
import time
backup_disk_path = "/media/encrypteddrive-sda/"
backups_folder_path = os.path.join(backup_disk_path, "Backups/")


# Helper class for statistics
# class Disk_Statistics(object):
#     def __init__(self):
#         self.total = 0
#         self.used = 0
#         self.free = 0
#         self.update_disc_usage()
#
#     def update_disc_usage(self):
#         old_used = self.used
#         old_free = self.free
#         self.total, self.used, self.free = shutil.disk_usage(backup_disk_path)
#         if [(old_used == self.used) or (old_free == self.free)]:
#             raise Exception("The values didn't change. \n Used: %d/%d \n Free: %d/%d" % (old_used,self.used, old_free,self.free))
#
#     def get_used_space_percent(self):
#         return (self.used/self.total)*100
#
#
# disk_statistics = Disk_Statistics()

while psutil.disk_usage(backup_disk_path).percent > 52:
    print("%d %% of disk %s are used. Freeing space..." % (psutil.disk_usage(backup_disk_path).percent,backup_disk_path))
    for primary_directory in os.listdir(backups_folder_path):
        primary_directory = os.path.join(backups_folder_path, primary_directory)
        for application_directory in os.listdir(primary_directory):
            time.sleep(5)
            application_directory = os.path.join(primary_directory, application_directory)
            diffs_directory = os.path.join(application_directory, "diffs/")
            diffs = os.listdir(diffs_directory)
            diffs.sort(reverse=False)
            delete_diff = diffs_directory + diffs[0]
            print("Deleting %s and free %s space..." % (delete_diff))
            #shutil.rmtree(delete_diff)
            #disk_statistics.update_disc_usage()

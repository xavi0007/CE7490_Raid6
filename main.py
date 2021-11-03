import sys
import os
import sys

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_DIR)
PAR_PATH = os.path.abspath(os.path.join(ROOT_DIR, os.pardir))
sys.path.append(PAR_PATH)

from RAID_File.raid_6 import RAID
from files import File
from partitions import DiskObject
import logging

logging.basicConfig(filename='disk.log', level=logging.INFO)

RAID_settings = {
    'num_disk' : 4,
    'num_non_parity_disk' : 2,
    'num_parity_disk': 2,
    'size_of_disk': 16, #in bits
    'root_dir' : '/Users/xavier/Documents/NTU/CE7490/Assignment_2/RAID-6/C_drive',
}

def main():

    logging.info("-----------------Set up the RAID 6 system-----------------")
    all_disk = []
    for idx in range(RAID_settings['num_disk']):
        all_disk.append(DiskObject(disk_path=RAID_settings['root_dir'], id=idx, disk_size=RAID_settings['size_of_disk']))

    #store all the data as per normal, first 2 disk is normal
    # normal_disk = DiskObject(disk_path=RAID_settings['root_dir'], id=-1, disk_size=RAID_settings['num_non_parity_disk'])
    normal_disk = all_disk[:RAID_settings['num_non_parity_disk']]

    #init raid for the disks
    raid_6 = RAID(disk_list=all_disk)

    

    # Random Generate some files and store into logical disk
    file = File()
    file.random_generate_string(data_size=RAID_settings['size_of_disk'])
    normal_disk.write_to_disk(disk=logical_disk, data=file.file_content)
    data_block_list = logical_disk.set_up_data_block_list(block_size=conf.block_size)

    # Load the data block from logical disk into RAID 6
    Logger.log_str("-----------------Write the file to RAID 6-----------------")

    raid_6.write_file(data_block_list=data_block_list)
    raid_6.read_from_disk_and_generate_data()

    Logger.log_str("-----------------Test silent corruption-----------------")

    # Start the test of raid 6
    data = raid_6.read_all_data_disks()
    raid_6.check_corruption(disk_data_in_int=data)

    Logger.log_str("-----------------Test data recovery-----------------")
    # Start to do the recover test
    corrupted_disk_list = (6, 7)
    for disk_id in corrupted_disk_list:
        with open(file=os.path.join(raid_6.disk_list[disk_id].disk_path, 'data'), mode='w') as f:
            f.write("")
            Logger.log_str('Disk {}\'s data is erased'.format(disk_id))

    raid_6.recover_disk(corrupted_disk_index=(6, 7))
    raid_6.read_from_disk_and_generate_data()

    # Update one char in file and re-generate
    Logger.log_str("-----------------Test data update-----------------")

    file.update(index=0, new_char='t')
    logical_disk.write_to_disk(disk=logical_disk, data=file.file_content)
    data_block_list = logical_disk.set_up_data_block_list(block_size=conf.block_size)
    for i, new_data, old_data in zip(range(len(data_block_list)), data_block_list, raid_6.data_block_list):
        if new_data != old_data:
            raid_6.update_data(block_global_index=i, new_data_block=new_data)
            break

    raid_6.read_from_disk_and_generate_data()

    # Update one char in file and re-generate

    file.update(index=1, new_char='d')
    logical_disk.write_to_disk(disk=logical_disk, data=file.file_content)
    data_block_list = logical_disk.set_up_data_block_list(block_size=conf.block_size)
    for i, new_data, old_data in zip(range(len(data_block_list)), data_block_list, raid_6.data_block_list):
        if new_data != old_data:
            raid_6.update_data(block_global_index=i, new_data_block=new_data)
            break

    raid_6.read_from_disk_and_generate_data()


if __name__ == '__main__':
    main()

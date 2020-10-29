import constants
import subprocess
import datetime
import os

def make_tmp_dir():
    '''
    create a tmp directory
    '''
    subprocess.run("mkdir "+constants.TMP_DIR_PATH, shell=True)

def del_tmp_dir():
    '''
    delete the tmp directory
    '''
    subprocess.run("rm -r "+constants.TMP_DIR_PATH, shell=True)

def zip_dir(dir_path, machine_name):
    '''
    Create a zip archive of a directory
    dir_path: path to the directory to compress
    machine_name: used to create the archive's name
    '''
    timestamp = str(int(datetime.datetime.now().timestamp()))
    arch_name = machine_name+"_"+timestamp+".zip"
    target_dir = dir_path[0:-(len(dir_path.split("/")[-1]))]
    subprocess.run("zip -r -qq "+target_dir + arch_name+" "+dir_path+"/*", shell=True)
    return target_dir + arch_name

def move_archive(archive_name, machine_name):
    '''
    Move the zip archive into the backup folder
    archive_name: the name of the zip archive
    machine_name: the name of the machine for which we run a backup
    '''
    subprocess.run("mv "+archive_name+" "+constants.BACKUP_FOLDER[machine_name], shell=True)

def del_file(file_name, dir_name):
    '''
    Delete a file in a directory
    file_name: the file to be deleted
    dir_name: directory of the file
    '''
    subprocess.run("rm -r "+dir_name+"/"+file_name, shell=True)

def cleanup_backup_folder(machine_name):
    '''
    if too many backups are stored remove the oldest one 
    (constants.NO_OF_BACKUP_VERSIONS is the number of backups that are kept)
    machine_name: the name of the machine that is being backed up
    '''
    backup_dir = constants.BACKUP_FOLDER[machine_name]
    while len([name for name in os.listdir(backup_dir)])>constants.NO_OF_BACKUP_VERSIONS:
        #remove oldest backup
        oldest_backup = ""
        oldest_timestamp = 0
        names = [name for name in os.listdir(backup_dir)]
        for name in names:
            timestamp = int(name.split("_")[-1].split(".")[0])
            if timestamp<oldest_timestamp or oldest_timestamp==0:
                # make current backup the oldest one
                oldest_backup = name
                oldest_timestamp = timestamp
        # Delete the oldest backup file
        del_file(file_name=oldest_backup, dir_name=backup_dir)
        


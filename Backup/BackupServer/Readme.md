# How to configure the Backup Server
There are two ways to backup your files using this backup server:

1) Let the backup server read from the filesystem where the files are stored that you want to backup. For that simply add the absolute path to the file or directory into the  `Backup_file_list_<MACHINE_NAME>.txt` which can be found in this directory. File path should be of the following form: `
/home/ubuntu/coucou` and foder path of the following: `/home/ubuntu/test/*`. 


*NOTE:* To check if the backup was successfull go into the backup driectory on the backup server and unzip the latest backup (the one with the biggest timestamp in the archive's name) (` ~/backup_<MACHINE_NAME>`). Also keep in mind that the `backup_user` gives itself read access to the files that need to be backed up (This won't affect the access permissions for any other user). So it can run `setaclf` as sudo without the need to enter a password.

2) Dump your file(s) into the `backup_dir` on your own machine, go into the file [constants.py](./constants.py) and set the value in the `BACKUP_LETTERBOX` dict of your machine to True.

**IMPORTANT:** The files you dump into the `backup_dir` will be removed after backing them up.

*NOTE:* The "letterbox" will be backed up into the same backup directory on the backup server as the backup from version 1.

*GENERAL NOTE:* The backups from version 1. are not kept forever (to save space) only [NO_OF_BACKUP_VERSIONS](./constants.py) (10) versions of the backup are stored on the backup server. However, the "letterboxes" are stored indefinitely. It is therefore important that you don't dump too much data regularly into the `backup_dir` on your machine. Furthermore, the backup is run automatically once an hour. Therefore, if you place multiple things into the `backup_dir` within an hour then these files need to have unique names.

## How to test the Backup Server
If you don't want to wait an hour to see if the automatic backup worked then simply run [`./server`](./server) from this directory.

The backups can be found in the folder `~/backup_<MACHINE_NAME>`. Version 1 backups are called `<MACHINE_NAME>_<TIME_STAMP>.zip` and version 2 backups are called `letterbox_<MACHINE_NAME>_<TIME_STAMP>.zip`
import pysftp
import datetime
import constants
import os
from stat import S_ISDIR

class SFTP:
    def __init__(self, host_ip, username, key_file):
        self.host_ip = host_ip
        self.username = username
        self.key_file = key_file
    
    def is_online(self):
        '''
        Is the sftp host reachable?
        '''
        try:
            with pysftp.Connection(host=self.host_ip, username=self.username, private_key =self.key_file) as sftp:
                return True
        except Exception:
            return False
    
    def get(self, path, local_dir):
        '''
        Parse a path and depending on if we back up a folder or a single file 
        perform the backup accordingly.
        path: line from the backup file list
        local_dir: directory to where the file or folder should be backed up
        '''
        # Remove line breaks from the path
        path = path.replace('\r', '').replace('\n', '')
        if path.split("/")[-1]=="*":
            # Path points to a directory
            folder_name = path.split("/")[-2]
            remote_dir = path[0:-(len(folder_name)+2)]
            try:
                if remote_dir=="/":
                    remote_dir=2*"../" #TODO: this is a bit a hacky solution... but "/" doesn't work for some reason...
                self.getDir(folder_name=folder_name, remote_dir=remote_dir, local_dir=local_dir)
            except Exception:
                print("ERROR: getDir("+folder_name+", "+remote_dir+", "+local_dir+") failed!")
            finally:
                pass
            
        else:
            # Path points to a single file
            file_name = path.split("/")[-1]
            remote_dir = path[0:-(len(file_name))]
            try:
                self.getFile(file_name=file_name, remote_dir=remote_dir, local_dir=local_dir)
            except Exception:
                print("ERROR: getFile("+file_name+", "+remote_dir+", "+local_dir+") failed!")
            finally:
                pass
            


    def getDir(self, folder_name, remote_dir, local_dir):
        '''
        Backup an entire directory recursively (with all subdirectories)
        folder_name: Name of the folder on the remote
        remote_dir: Path to where "folder_name" is located
        local_dir: Path to the directory where "folder_name" should be backed up
        '''
        with pysftp.Connection(host=self.host_ip, username=self.username, private_key =self.key_file) as sftp:
            # Copy full folder hirarchy at remote_dir to local_dir
            with sftp.cd(remote_dir[0:-1]) as cd:
                sftp.get_r(remotedir=folder_name, localdir=local_dir)

    def getFile(self, file_name, remote_dir, local_dir):
        '''
        Back up a single file.
        file_name: Name of the file on the remote
        remote_dir: Path to where "file_name" is located
        local_dir: Path to the directory where "file_name" should be backed up
        '''
        with pysftp.Connection(host=self.host_ip, username=self.username, private_key=self.key_file) as sftp:
            # Assemble the path where the file should be stored
            localFilePath = local_dir+"/"+file_name
            # Assemble the path from where we get the file on the remote host
            remoteFilePath = remote_dir+file_name
            sftp.get(remotepath=remoteFilePath, localpath=localFilePath)

    def putFile(self, file_name, remote_dir, local_dir):
        '''
        Restore a single file.
        file_name: Name of the file which is to be restored
        remote_dir: Path to where "file_name" should be put
        local_dir: Path to the directory where "file_name" is located
        '''
        with pysftp.Connection(host=self.host_ip, username=self.username, private_key=self.key_file) as sftp:
            # Assemble the path from where we get the file that we want to send to the remote host
            localFilePath = local_dir+file_name
            # Assemble the path to where we want to send the file on the remote host
            remoteFilePath = remote_dir+file_name
            sftp.put(remotepath=remoteFilePath, localpath=localFilePath)
    
    def empty_letterbox(self, local_dir):#TODO: that doesn't seem to work
        '''
        Empty the letterbox
        local_dir: this is where the letter box is saved
        '''
        # Back up the content of the letterbox
        self.get(path=constants.BACKUP_DIR+"*", local_dir=local_dir)
        #self.getDir(constants.BACKUP_DIR[1:], "/", local_dir)
        # remove the letterbox
        self.reset_letterbox()
        
    def reset_letterbox(self):
        '''
        Delete the content of the letter box on the remote
        '''
        with pysftp.Connection(host=self.host_ip, username=self.username, private_key=self.key_file) as sftp:
            files = sftp.listdir(remotepath=constants.BACKUP_DIR)
            for f in files:
                filepath = os.path.join(constants.BACKUP_DIR, f)
                if self.isdir(filepath):
                    self.rmdir(filepath)
                else:
                    sftp.remove(filepath)
        

    def isdir(self, path):
        '''
        True iff path is a directory
        path: path to test
        '''
        with pysftp.Connection(host=self.host_ip, username=self.username, private_key=self.key_file) as sftp:
            try:
                return S_ISDIR(sftp.stat(path).st_mode)
            except IOError:
                return False

    def rmdir(self, path):
        '''
        Remove the directory with all its content
        path: path of the directory on the remote
        '''
        with pysftp.Connection(host=self.host_ip, username=self.username, private_key=self.key_file) as sftp:
            files = sftp.listdir(remotepath=path)
            for f in files:
                filepath = os.path.join(path, f)
                if isdir(filepath):
                    self.rmdir(filepath)
                else:
                    sftp.remove(filepath)
            sftp.rmdir(path)

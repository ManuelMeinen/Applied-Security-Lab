# Names of the machines
NAME_CORE = "Core"
NAME_CA = "CA"
NAME_MYSQL_DATABASE = "MySQLDatabase"
NAME_FIREWALL = "Firewall"
NAME_WEB_SERVER = "WebServer"
NAME_VPN = "VPN"
NAMES = [NAME_CORE, NAME_CA, NAME_MYSQL_DATABASE, NAME_FIREWALL, NAME_WEB_SERVER, NAME_VPN]
# IP addresses of the machines
IP_ADDRESSES = {
    NAME_CORE:"10.0.20.10",
    NAME_CA:"10.0.20.20",
    NAME_MYSQL_DATABASE:"10.0.20.30",
    NAME_FIREWALL:"10.0.20.40",
    NAME_WEB_SERVER:"192.168.1.20",
    NAME_VPN:"192.168.1.30"
}
# Backup file lists
BACKUP_FILE_LIST = {
    NAME_CORE:"Backup_file_list_"+NAME_CORE+".txt",
    NAME_CA:"Backup_file_list_"+NAME_CA+".txt",
    NAME_MYSQL_DATABASE:"Backup_file_list_"+NAME_MYSQL_DATABASE+".txt",
    NAME_FIREWALL:"Backup_file_list_"+NAME_FIREWALL+".txt",
    NAME_WEB_SERVER:"Backup_file_list_"+NAME_WEB_SERVER+".txt",
    NAME_VPN:"Backup_file_list_"+NAME_VPN+".txt"
}
# Paths of backup folders
BACKUP_FOLDER = {
    NAME_CORE:"/home/ubuntu/backup_"+NAME_CORE,
    NAME_CA:"/home/ubuntu/backup_"+NAME_CA,
    NAME_MYSQL_DATABASE:"/home/ubuntu/backup_"+NAME_MYSQL_DATABASE,
    NAME_FIREWALL:"/home/ubuntu/backup_"+NAME_FIREWALL,
    NAME_WEB_SERVER:"/home/ubuntu/backup_"+NAME_WEB_SERVER,
    NAME_VPN:"/home/ubuntu/backup_"+NAME_VPN
}
# Backup letterbox
BACKUP_LETTERBOX = {
    NAME_CORE:True,
    NAME_CA:False,
    NAME_MYSQL_DATABASE:True,
    NAME_FIREWALL:False,
    NAME_WEB_SERVER:False,
    NAME_VPN:False
}
# User names
USER_UBUNTU = "ubuntu"
USER_BACKUP = "backup_user"
# Key path
KEY_PATH = "/home/ubuntu/.ssh/backup_sftp_key"

BACKUP_DIR = "/backup_dir/"
BACKUP_DIR_MODE = 703
HOME_PATH = "/home/ubuntu/"
TMP_DIR_PATH = "/home/ubuntu/tmp"
TMP_DIR_PATH_2 = "/home/ubuntu/tmp_2"
LETTERBOX_TAG = "letterbox_"
CODE_BASE_DIR = "/home/ubuntu/BackupServer/"

NO_OF_BACKUP_VERSIONS = 10

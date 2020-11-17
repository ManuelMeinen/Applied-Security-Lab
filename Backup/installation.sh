#!/bin/bash
echo "Installation script started"

# Copy SSH keys to the right directory
cp /media/asl/Backup/backup_sftp_key /home/ubuntu/.ssh/
cp /media/asl/Backup/backup_sftp_key.pub /home/ubuntu/.ssh/
cp /media/asl/Backup/known_hosts /home/ubuntu/.ssh/
chmod 700 /home/ubuntu/.ssh/backup_sftp_key #Private key only readable by root

# Install pysftp and python3
apt-get update
apt-get upgrade -y
apt-get -y install python3 python3-pip zip cron ifupdown
python3 -m pip install pysftp

# Permanently configure networking stuff
cp /media/asl/Backup/net_setup /etc/network/if-up.d/
chmod +x /etc/network/if-up.d/net_setup
/etc/network/if-up.d/net_setup

# Setup backup directories (only root can read the backups)
mkdir /home/ubuntu/backup_MySQLDatabase
chmod 711 /home/ubuntu/backup_MySQLDatabase
mkdir /home/ubuntu/backup_Core
chmod 711 /home/ubuntu/backup_Core
mkdir /home/ubuntu/backup_CA
chmod 711 /home/ubuntu/backup_CA
mkdir /home/ubuntu/backup_Firewall
chmod 711 /home/ubuntu/backup_Firewall
mkdir /home/ubuntu/backup_WebServer
chmod 711 /home/ubuntu/backup_WebServer
mkdir /home/ubuntu/backup_VPN
chmod 711 /home/ubuntu/backup_VPN

# Copy the BackupServer Codebase
mkdir /home/ubuntu/BackupServer
cp /media/asl/Backup/BackupServer/* /home/ubuntu/BackupServer
chown root:root /home/ubuntu/BackupServer/*
# Change permissions in code base (only root can add files to be backed up)
chmod 600 /home/ubuntu/BackupServer/Backup_file_list_CA.txt
chmod 600 /home/ubuntu/BackupServer/Backup_file_list_Core.txt
chmod 600 /home/ubuntu/BackupServer/Backup_file_list_Firewall.txt
chmod 600 /home/ubuntu/BackupServer/Backup_file_list_MySQLDatabase.txt
chmod 600 /home/ubuntu/BackupServer/Backup_file_list_VPN.txt
chmod 600 /home/ubuntu/BackupServer/Backup_file_list_WebServer.txt


# Run backup every hour (as root --> run sudo crontab -l to list the job)
echo "0 * * * * /home/ubuntu/BackupServer/server >> /home/ubuntu/BackupServer/backup_log.txt" | crontab -

#!/bin/bash
echo "Installation script started"

# Copy SSH keys to the right directory
cp /media/asl/Backup/backup_sftp_key /home/ubuntu/.ssh/
cp /media/asl/Backup/backup_sftp_key.pub /home/ubuntu/.ssh/
cp /media/asl/Backup/known_hosts /home/ubuntu/.ssh/
chmod 755 /home/ubuntu/.ssh/backup_sftp_key

# Install pysftp and python3
apt-get update
apt-get upgrade -y
apt-get -y install python3 python3-pip zip
python3 -m pip install pysftp

# Setup backup directories
mkdir ~/backup_MySQLDatabase
chmod 777 ~/backup_MySQLDatabase
mkdir ~/backup_Core
chmod 777 ~/backup_Core
mkdir ~/backup_CA
chmod 777 ~/backup_CA
mkdir ~/backup_Firewall
chmod 777 ~/backup_Firewall
mkdir ~/backup_WebServer
chmod 777 ~/backup_WebServer
mkdir ~/backup_VPN
chmod 777 ~/backup_VPN

# Copy the BackupServer Codebase
mkdir ~/BackupServer
cp /media/asl/Backup/BackupServer/* ~/BackupServer
chown ubuntu:ubuntu ~/BackupServer/*


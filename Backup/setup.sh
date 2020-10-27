#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 10.0.20.50 netmask 255.255.255.0 up
ip route add 192.168.1.0/24 via 10.0.20.40

# Copy SSH keys to the right directory
cp /media/asl/Backup/backup_sftp_key /home/ubuntu/.ssh/
cp /media/asl/Backup/backup_sftp_key.pub /home/ubuntu/.ssh/
cp /media/asl/Backup/known_hosts /home/ubuntu/.ssh/
chmod 755 /home/ubuntu/.ssh/backup_sftp_key

# Install pysftp and python3
apt-get update
apt-get upgrade -y
apt-get -y install python3 python3-pip
python3 -m pip install pysftp

# Setup backup directories
mkdir ~/backup_MySQLDatabase
chmod 1711 ~/backup_MySQLDatabase
mkdir ~/backup_Core
chmod 1711 ~/backup_Core
mkdir ~/backup_CA
chmod 1711 ~/backup_CA
mkdir ~/backup_Firewall
chmod 1711 ~/backup_Firewall
mkdir ~/backup_WebServer
chmod 1711 ~/backup_WebServer
mkdir ~/backup_VPN
chmod 1711 ~/backup_VPN

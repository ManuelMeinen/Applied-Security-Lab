#!/bin/bash

# Permanently configure networking stuff
echo "Setup startup"
cp /media/asl/Firewall/startup.service /etc/systemd/system
mkdir /etc/startup
cp /media/asl/Firewall/startup /etc/startup
chmod +x /etc/startup/startup
service startup start
systemctl enable startup

# Adding a backup_user
userdel -r backup_user
username="backup_user"
password="rS^9cN?E?jxTj@4K"
pass=$(perl -e 'print crypt($ARGV[0], "password")' $password)
useradd -m -p "$pass" "$username"
adduser "$username" sudo
# Create Backup Directory
mkdir "/backup_dir"
chown "backup_user" "/backup_dir"
chmod 0703 "/backup_dir"
#SFTP keys for login without password
mkdir /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh
cp /media/asl/Firewall/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys

#!/bin/bash
# Install stuff...
apt-get update
apt-get upgrade -y
apt-get -y install ifupdown

# Permanently configure networking stuff
cp /media/asl/Firewall/net_setup /etc/network/if-up.d/
chmod +x /etc/network/if-up.d/net_setup
/etc/network/if-up.d/net_setup

# Adding a backup_user
username="backup_user"
password="ubuntu" #TODO: change the password
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

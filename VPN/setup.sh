#!/bin/bash
echo "Setup VPN"


# Create VPN connection with wireguard
cp /media/asl/VPN/wg_private /home/ubuntu/.ssh/


# Adding a backup_user
userdel -r backup_user
username="backup_user"
password="	?c_bEpuN-ssCJ4Y3"
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
cp /media/asl/VPN/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys

echo "Setup startup"
cp /media/asl/VPN/startup.service /etc/systemd/system
mkdir /etc/startup
cp /media/asl/VPN/startup /etc/startup
chmod +x /etc/startup/startup
service startup start
systemctl enable startup
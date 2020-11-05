#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 10.0.20.30 netmask 255.255.255.0 up
ip route add 192.168.1.0/24 via 10.0.20.40

#Allow SFTP connetions to Backup Server
iptables -A INPUT -i enp0s3 -s 10.0.20.50 -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -d 10.0.20.50 -p tcp --sport 22 -j ACCEPT
# Adding a backup_user
username="backup_user"
password="ubuntu" #TODO: change the password
pass=$(perl -e 'print crypt($ARGV[0], "password")' $password)
useradd -m -p "$pass" "$username"
adduser "$username" sudo
# Create Backup Directory
mkdir "backup_dir"
chown "backup_user" "backup_dir"
chmod 0703 "backup_dir"
#SFTP keys for login without password
mkdir /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh
cp /media/asl/MySQLDatabase/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys
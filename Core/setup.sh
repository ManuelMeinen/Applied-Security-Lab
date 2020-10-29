#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 10.0.20.10 netmask 255.255.255.0 up
ifconfig enp0s8 10.0.10.10 netmask 255.255.255.0 up
ip route add 192.168.1.0/24 via 10.0.10.40
ip route add 192.168.1.30/32 via 10.0.20.40

apt install -y python3-pip
pip3 install requests
cp /media/asl/CA/cacert.pem /home/ubuntu/cacert.pem
cp /media/asl/Core/flask_client.py /home/ubuntu

mkdir /etc/Flask
mkdir /etc/Flask/private
mkdir /etc/Flask/certs
cp /media/asl/Core/core_cert.pem /etc/Flask/certs/core_cert.pem
cp /media/asl/Core/core_key.pem /etc/Flask/private/core_key.pem

echo "10.0.20.20    ca_server" >> /etc/hosts

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
cp /media/asl/Core/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys

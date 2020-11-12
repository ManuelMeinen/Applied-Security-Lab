#!/bin/bash
echo "Setup environment"
ifconfig enp0s3 10.0.20.10 netmask 255.255.255.0 up
ifconfig enp0s8 10.0.10.10 netmask 255.255.255.0 up
ip route add 192.168.1.0/24 via 10.0.10.40
ip route add 192.168.1.30/32 via 10.0.20.40

# Install dependencies
# sh /media/asl/Core/installation.sh

echo "nameserver 8.8.8.8" > /etc/resolv.conf

cp /media/asl/Core/flask_client.py /home/ubuntu
cp /media/asl/Core/flask_client2.py /home/ubuntu

echo "10.0.20.20    ca_server" >> /etc/hosts
echo "127.0.0.1   core" >> /etc/hosts

#Allow SFTP connetions to Backup Server
iptables -A INPUT -i enp0s3 -s 10.0.20.50 -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -d 10.0.20.50 -p tcp --sport 22 -j ACCEPT

# Adding a backup_user
userdel -r backup_user
username="backup_user"
password="7zM2YCHky=SQ?e3n"
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
cp /media/asl/Core/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys

# Flask server
mkdir /var/www
mkdir /var/www/core
mkdir /etc/Flask
mkdir /etc/Flask/private
mkdir /etc/Flask/certs
cp /media/asl/Core/core_cert.pem /etc/Flask/certs/core_cert.pem
cp /media/asl/Core/core_key.pem /etc/Flask/private/core_key.pem
cp /media/asl/CA/cacert.pem /etc/Flask/certs/cacert.pem
cp /media/asl/Core/flask_server.py /var/www/core

python3 /var/www/core/flask_server.py > /var/log/Flask.log 2>&1 

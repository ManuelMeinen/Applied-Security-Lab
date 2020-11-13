#!/bin/bash
# echo "Nothing to be set up..."
ifconfig enp0s3 192.168.1.20 netmask 255.255.255.0 up
ip route add 10.0.10.10 via 192.168.1.40
ip route add 10.0.20.50 via 192.168.1.40

# Add hosts
echo "10.0.10.10    core" >> /etc/hosts

#Allow SFTP connetions to Backup Server
iptables -A INPUT -i enp0s3 -s 10.0.20.50 -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -d 10.0.20.50 -p tcp --sport 22 -j ACCEPT
# Adding a backup_user
userdel -r backup_user
username="backup_user"
password="C?NMuPu77c4sHfa3"
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
cp /media/asl/WebServer/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys

#Install necessary software and library
apt update 
apt upgrade -y
apt install python3-pip -y
pip3 install requests Flask

#Allow http request to Core Server
iptables -A OUTPUT -d 10.0.10.10 -p tcp --sport 443 -j ACCEPT
iptables -A INPUT -i enp0s3 -s 10.0.10.10 -p tcp --dport 433 -j ACCEPT

#Copy webpages, scripts and configuration files
cp /media/asl/WebServer/webserver_cert.pem /etc/ssl/certs/webserver_cert.pem
cp /media/asl/WebServer/webserver_key.pem /etc/ssl/private/webserver_key.pem
cp /media/asl/Core/core_cert.pem /etc/ssl/certs/core_cert.pem

mkdir /var/www/webserver/
cp /media/asl/WebServer/webserver_flask.py /var/www/webserver/webserver_flask.py

mkdir /var/www/webserver/templates
cp /media/asl/WebServer/templates/login.html /var/www/webserver/templates/login.html
cp /media/asl/WebServer/templates/home.html /var/www/webserver/templates/home.html

#Run server
python3 /var/www/webserver/webserver_flask.py






# TODO:
# - configure files access right
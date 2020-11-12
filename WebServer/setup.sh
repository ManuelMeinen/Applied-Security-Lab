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
cp /media/asl/WebServer/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys
# # Adding a backup_user
# username="backup_user"
# password="ubuntu" #TODO: change the password
# pass=$(perl -e 'print crypt($ARGV[0], "password")' $password)
# useradd -m -p "$pass" "$username"
# adduser "$username" sudo
# # Create Backup Directory
# mkdir "backup_dir"
# chown "backup_user" "backup_dir"
# chmod 0703 "backup_dir"
# #SFTP keys for login without password
# mkdir /home/backup_user/.ssh
# chmod 755 /home/backup_user/.ssh
# cp /media/asl/WebServer/authorized_keys /home/backup_user/.ssh
# chmod 755 /home/backup_user/.ssh/authorized_keys



#Install necessary software and library
# apt update 
# apt upgrade -y
# tasksel install lamp-server
# apt install php libapache2-mod-php

#Copy webpages and configuration files
cp /media/asl/WebServer/000-default.conf /etc/apache2/sites-available/000-default.conf
cp /media/asl/WebServer/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf
cp /media/asl/WebServer/webserver_cert.pem /etc/ssl/certs/webserver_cert.pem
cp /media/asl/WebServer/webserver_key.key /etc/ssl/private/webserver_key.key

cp /media/asl/WebServer/index.php /var/www/html/index.php
cp /media/asl/WebServer/login.php /var/www/html/login.php
cp /media/asl/WebServer/logout.php /var/www/html/logout.php

#Enable website
a2enmod ssl
a2enmod php7.2
a2ensite 000-default.conf
a2ensite default-ssl.conf
systemctl restart apache2.service

#Allow http request to Core Server
iptables -A OUTPUT -d 10.0.10.10 -p tcp --sport 443 -j ACCEPT
iptables -A INPUT -i enp0s3 -s 10.0.10.10 -p tcp --dport 433 -j ACCEPT






# TODO:
# - configure files access right
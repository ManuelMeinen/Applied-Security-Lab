#!/bin/bash
# echo "Nothing to be set up..."
# ifconfig enp0s3 192.168.1.20 netmask 255.255.255.0 up
# ip route add 10.0.10.10 via 192.168.1.40
# ip route add 10.0.20.50 via 192.168.1.40

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

# #Install web server
# apt update 
# apt upgrade -y
# apt install -y apache2

#Copy HTML pages, virtual host configuration, certificate and key
cp /media/asl/WebServer/000-default.conf /etc/apache2/sites-available/000-default.conf
cp /media/asl/WebServer/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf
cp /media/asl/WebServer/asl.ch.crt /etc/ssl/certs/asl.ch.crt
cp /media/asl/WebServer/asl.ch.key /etc/ssl/private/asl.ch.key

cp /media/asl/WebServer/index.html /var/www/html/index.html
cp /media/asl/WebServer/login.html /var/www/html/login.html
cp /media/asl/WebServer/main.html /var/www/html/main.html
cp /media/asl/WebServer/ca_admin.html /var/www/html/ca_admin.html
cp /media/asl/WebServer/cert_issue.html /var/www/html/cert_issue.html
cp /media/asl/WebServer/cert_revoc.html /var/www/html/cert_revoc.html

cp /media/asl/WebServer/login.php /var/www/html/login.php

#Test config
sudo apachectl configtest

#Enable server configuration and disable the default one
a2enmod rewrite
a2enmod ssl
a2ensite default-ssl
a2ensite 000-default

#Restart apache to take change into account
systemctl restart apache2.service


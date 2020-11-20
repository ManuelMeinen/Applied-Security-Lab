#!/bin/bash
# echo "Nothing to be set up..."


# Add hosts
echo "10.0.10.10    core" >> /etc/hosts
echo "nameserver 8.8.8.8" > /etc/resolv.conf


# Adding a backup_user
userdel -r backup_user
username="backup_user"
password="C?NMuPu77c4sHfa3"
pass=$(perl -e 'print crypt($ARGV[0], "password")' $password)
useradd -m -p "$pass" "$username"
adduser "$username" sudo
cp /media/asl/WebServer/sudoers /etc

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
pip3 install Flask-WTF

#Copy webpages, scripts and configuration files
cp /media/asl/WebServer/webserver_cert.pem /etc/ssl/certs/webserver_cert.pem
cp /media/asl/WebServer/webserver_key.pem /etc/ssl/private/webserver_key.pem
cp /media/asl/Core/core_cert.pem /etc/ssl/certs/core_cert.pem
cp /media/asl/CA/cacert.pem /etc/ssl/certs/cacert.pem

mkdir -p /var/www/webserver/
cp /media/asl/WebServer/webserver_flask.py /var/www/webserver/webserver_flask.py

mkdir -p /var/www/webserver/templates
cp /media/asl/WebServer/templates/login.html /var/www/webserver/templates/login.html
cp /media/asl/WebServer/templates/home.html /var/www/webserver/templates/home.html
cp /media/asl/WebServer/templates/account.html /var/www/webserver/templates/account.html
cp /media/asl/WebServer/templates/ca_admin.html /var/www/webserver/templates/ca_admin.html

mkdir /var/www/webserver/files

echo "Setup startup"
cp /media/asl/WebServer/startup.service /etc/systemd/system
mkdir /etc/startup
cp /media/asl/WebServer/startup /etc/startup
chmod +x /etc/startup/startup
service startup start
systemctl enable startup







# TODO:
# - configure files access right
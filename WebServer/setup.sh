#!/bin/bash

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

# Install dependencies
echo "Install depedencies"
sh /media/asl/WebServer/installation.sh

# Copy the certs and keys
mkdir /etc/Flask
mkdir /etc/Flask/private
mkdir /etc/Flask/certs
cp /media/asl/WebServer/webserver_cert.pem /etc/Flask/certs/webserver_cert.pem
chown ubuntu:root /etc/Flask/certs/webserver_cert.pem
chmod 640 /etc/Flask/certs/webserver_cert.pem
cp /media/asl/WebServer/webserver_key.pem /etc/Flask/private/webserver_key.pem
chown ubuntu:root /etc/Flask/private/webserver_key.pem
chmod 600 /etc/Flask/private/webserver_key.pem
cp /media/asl/CA/cacert.pem /etc/Flask/certs/cacert.pem
chown ubuntu:root /etc/Flask/certs/cacert.pem
chmod 640 /etc/Flask/certs/cacert.pem

#Nginx configuration
unlink /etc/nginx/sites-enabled/default
cp /media/asl/WebServer/reverse-proxy.conf /etc/nginx/sites-available/reverse-proxy.conf
chown root /etc/nginx/sites-available/reverse-proxy.conf
chmod 600 /etc/nginx/sites-available/reverse-proxy.conf
ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf
service nginx configtest
systemctl enable nginx
service nginx restart

#Copy webpages, scripts and configuration files
mkdir -p /var/www/webserver/
cp /media/asl/WebServer/webserver_flask.py /var/www/webserver/webserver_flask.py
chown ubuntu:root /var/www/webserver/webserver_flask.py
chmod 740 /var/www/webserver/webserver_flask.py

mkdir -p /var/www/webserver/templates
cp /media/asl/WebServer/templates/login.html /var/www/webserver/templates/login.html
chown ubuntu:root /var/www/webserver/templates/login.html
chmod 640 /var/www/webserver/templates/login.html
cp /media/asl/WebServer/templates/home.html /var/www/webserver/templates/home.html
chown ubuntu:root /var/www/webserver/templates/home.html
chmod 640 /var/www/webserver/templates/home.html
cp /media/asl/WebServer/templates/account.html /var/www/webserver/templates/account.html
chown ubuntu:root /var/www/webserver/templates/account.html
chmod 640 /var/www/webserver/templates/account.html
cp /media/asl/WebServer/templates/ca_admin.html /var/www/webserver/templates/ca_admin.html
chown ubuntu:root /var/www/webserver/templates/ca_admin.html
chmod 640 /var/www/webserver/templates/ca_admin.html

touch /var/log/Flask.log
chmod 640 /var/log/Flask.log
chown ubuntu:root /var/log/Flask.log

echo "Setup startup"
cp /media/asl/WebServer/startup.service /etc/systemd/system
mkdir /etc/startup
cp /media/asl/WebServer/startup /etc/startup
chmod +x /etc/startup/startup
service startup start
systemctl enable startup



# TODO:
# - configure files access right
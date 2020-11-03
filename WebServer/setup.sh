#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 192.168.1.20 netmask 255.255.255.0 up
ip route add 10.0.10.10 via 192.168.1.40
ip route add 10.0.20.50 via 192.168.1.40

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

#Install web server
apt update 
apt upgrade -y
apt install -y apache2
ufw allow 'Apache Full'

#Create directory
mkdir /var/www/asl_website
chown -R $USER:$USER /var/www/asl_website
chmod -R 755 /var/www/asl_website

#Copy HTML pages and virtual host configuration file
cp /media/asl/WebServer/index.html /var/www/asl_website
cp /media/asl/WebServer/asl_website.conf /etc/apache2/sites-available/asl_website.conf

#Enable server configuration and disable the default one
a2ensite asl_website.conf
a2dissite 000-default.conf
apache2ctl configtest

#Restart apache to take change into account
systemctl restart apache2


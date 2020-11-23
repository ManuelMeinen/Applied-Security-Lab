#!/bin/bash
echo "Setup environment"
echo "Setup network"

echo "nameserver 8.8.8.8" > /etc/resolv.conf
echo "nameserver 8.8.4.4" > /etc/resolv.conf
# Install dependencies
echo "Install depedencies"
sh /media/asl/Core/installation.sh


cp /media/asl/Core/flask_client3.py /home/ubuntu

echo "10.0.20.20    ca_server" >> /etc/hosts
echo "10.0.20.30    mysql" >> /etc/hosts
echo "127.0.0.1   core" >> /etc/hosts


# Adding a backup_user
userdel -r backup_user
username="backup_user"
password="7zM2YCHky=SQ?e3n"
pass=$(perl -e 'print crypt($ARGV[0], "password")' $password)
useradd -m -p "$pass" "$username"
adduser "$username" sudo
cp /media/asl/Core/sudoers /etc

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
chmod 644 /etc/Flask/certs/core_cert.pem
chown ubuntu:root /etc/Flask/certs/core_cert.pem
cp /media/asl/Core/core_key.pem /etc/Flask/private/core_key.pem
chmod 600 /etc/Flask/private/core_key.pem
chown ubuntu:root /etc/Flask/private/core_key.pem
cp /media/asl/CA/cacert.pem /etc/Flask/certs/cacert.pem
chmod 644 /etc/Flask/certs/cacert.pem
chown ubuntu:root /etc/Flask/certs/cacert.pem
cp /media/asl/Core/flask_server.py /var/www/core
chmod 700 /var/www/core/flask_server.py
chown ubuntu:root /var/www/core/flask_server.py
chmod 700 /bin/crons
cp /media/asl/Core/crons /bin
touch /var/log/Flask.log
chmod 640 /var/log/Flask.log
chown ubuntu:syslog /var/log/Flask.log

# Change password ubuntu YA&pd>I01>*h)6vjFT
echo -e "YA&pd>I01>*h)6vjFT\nYA&pd>I01>*h)6vjFT" | passwd ubuntu

echo "Setup startup"
cp /media/asl/Core/startup.service /etc/systemd/system
mkdir /etc/startup
cp /media/asl/Core/startup /etc/startup
chmod +x /etc/startup/startup
service startup start
systemctl enable startup

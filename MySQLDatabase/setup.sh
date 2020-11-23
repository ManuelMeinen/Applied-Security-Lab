#!/bin/bash
echo "sqlServer setup"


# Add hosts
#echo "10.0.20.10    core" >> /etc/hosts
#echo "10.0.20.30    mysql" >> /etc/hosts
cp -f /media/asl/MySQLDatabase/hosts /etc/hosts

echo "nameserver 8.8.8.8" > /etc/resolv.conf

#install mysql
echo "INSTALLATION OF MYSQL"
sh /media/asl/MySQLDatabase/installation.sh
echo "time to install mysql package"

#copy files for mysql
mkdir /var/www
mkdir /var/www/mysql
mkdir /etc/Flask
mkdir /etc/Flask/private
mkdir /etc/Flask/certs
cp /media/asl/MySQLDatabase/flask_server.py /var/www/mysql
chmod 740 /var/www/mysql/flask_server.py 
chown ubuntu:root /var/www/mysql/flask_server.py 
cp /media/asl/MySQLDatabase/sql_server.py /var/www/mysql
chmod 740 /var/www/mysql/sql_server.py
chown ubuntu:root /var/www/mysql/sql_server.py 
cp /media/asl/MySQLDatabase/imovies.sql /var/www/mysql
chmod 640 /var/www/mysql/imovies.sql 
cp /media/asl/MySQLDatabase/database_password.txt /var/www/mysql
chmod 600 /var/www/mysql/database_password.txt
chown ubuntu:root /var/www/mysql/database_password.txt
cp /media/asl/MySQLDatabase/mysql_cert.pem /etc/Flask/certs
chmod 640 /etc/Flask/certs/mysql_cert.pem
chown ubuntu:root /etc/Flask/certs/mysql_cert.pem
cp /media/asl/MySQLDatabase/mysql_key.pem /etc/Flask/private
chmod 600 /etc/Flask/private/mysql_key.pem
chown ubuntu:root /etc/Flask/private/mysql_key.pem
cp /media/asl/CA/cacert.pem /etc/Flask/certs/cacert.pem
chmod 640 /etc/Flask/certs/cacert.pem
chown ubuntu:root /etc/Flask/certs/cacert.pem
sudo mysql -u root < /var/www/mysql/imovies.sql &

cp -f /media/asl/MySQLDatabase/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf
touch /var/log/Flask.log
chmod 640 /var/log/Flask.log
chown ubuntu:root /var/log/Flask.log




echo "MYSQL INSTALLED"


# Adding a backup_user
username="backup_user"
password="ubuntu" #TODO: change the password
pass=$(perl -e 'print crypt($ARGV[0], "password")' $password)
useradd -m -p "$pass" "$username"
adduser "$username" sudo
cp /media/asl/MySQLDatabase/sudoers /etc

# Create Backup Directory
mkdir "/backup_dir"
chown "backup_user" "/backup_dir"
chmod 0703 "/backup_dir"

# SFTP keys for login without password
mkdir /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh
cp /media/asl/MySQLDatabase/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys

cp /media/asl/MySQLDatabase/test_server.py /home/ubuntu
cp /media/asl/MySQLDatabase/imovies.sql /backup_dir

# Change password ubuntu l6C)XRhH!P9iuFvTVa
echo -e "l6C)XRhH!P9iuFvTVa\nl6C)XRhH!P9iuFvTVa" | passwd ubuntu

echo "Setup startup"
cp /media/asl/MySQLDatabase/startup.service /etc/systemd/system
mkdir /etc/startup
cp /media/asl/MySQLDatabase/startup /etc/startup
chmod +x /etc/startup/startup
service startup start
systemctl enable startup

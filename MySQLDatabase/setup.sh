#!/bin/bash
echo "sqlServer setup"
ifconfig enp0s3 10.0.20.30 netmask 255.255.255.0 up
ip route add 192.168.1.0/24 via 10.0.20.40

# Add hosts
echo "10.0.20.10    core" >> /etc/hosts
echo "10.0.20.30    mysql" >> /etc/hosts

#install mysql
echo "INSTALLATION OF MYSQL"
#sh /media/asl/MySQLDatabase/installation.sh
echo "time to install mysql package"

#copy files for mysql
mkdir /var/www
mkdir /var/www/mysql
mkdir /etc/Flask
mkdir /etc/Flask/private
mkdir /etc/Flask/certs
cp /media/asl/MySQLDatabase/flask_server.py /var/www/mysql
cp /media/asl/MySQLDatabase/sql_server.py /var/www/mysql
cp /media/asl/MySQLDatabase/imovies.sql /var/www/mysql
cp /media/asl/MySQLDatabase/database_password.txt /var/www/mysql
chmod 700 /var/www/mysql/database_password.txt
cp /media/asl/MySQLDatabase/mysql_cert.pem /etc/Flask/certs
cp /media/asl/MySQLDatabase/mysql_key.pem /etc/Flask/private
cp /media/asl/CA/cacert.pem /etc/Flask/certs/cacert.pem
sudo mysql -u root < /var/www/mysql/imovies.sql &



echo "MYSQL INSTALLED"

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
SFTP keys for login without password
mkdir /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh
cp /media/asl/MySQLDatabase/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys

cp /media/asl/MySQLDatabase/test_server.py /home/ubuntu
python3 /var/www/mysql/flask_server.py > /var/log/Flask.log 2>&1 

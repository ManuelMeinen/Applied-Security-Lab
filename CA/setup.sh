#!/bin/bash
echo "Setup environment"
# Install dependencies
sh /media/asl/CA/installation.sh

# Setup CA
apt-get install -y openssl
mkdir /etc/ssl/CA
mkdir /etc/ssl/CA/certs
mkdir /etc/ssl/CA/newcerts
mkdir /etc/ssl/CA/private
mkdir /etc/ssl/CA/crl
touch /etc/ssl/CA/index.txt
touch /etc/ssl/CA/index.txt.attr
cp /media/asl/CA/openssl.cnf /etc/ssl/
cp /media/asl/CA/cakey.pem /etc/ssl/CA/private
cp /media/asl/CA/cacert.pem /etc/ssl/CA
cp /media/asl/CA/.rnd /home/ubuntu
echo "01" > /etc/ssl/CA/serial
echo "01" > /etc/ssl/CA/crlnumber
openssl ca -gencrl -out /etc/ssl/CA/crl/crl.pem -passin pass:ubuntu
cat /etc/ssl/CA/cacert.pem  /etc/ssl/CA/crl/crl.pem > /home/ubuntu/revoked.pem


echo "10.0.20.10    core" >> /etc/hosts
echo "nameserver 8.8.8.8" > /etc/resolv.conf



# Adding a backup_user
userdel -r backup_user
username="backup_user"
password="WR=JdhtW4R_qV4b9"
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
cp /media/asl/CA/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys

# Flask server
mkdir /var/www
mkdir /var/www/ca
mkdir /etc/Flask
mkdir /etc/Flask/private
mkdir /etc/Flask/certs

cp /media/asl/CA/ca_server_cert.pem /etc/Flask/certs/ca_cert.pem
cp /media/asl/CA/ca_server_key.pem /etc/Flask/private/ca_key.pem
cp /media/asl/CA/ca_server_key.pem /etc/Flask/private/ca_key.pem
cp /media/asl/CA/cacert.pem /etc/Flask/certs/
cp /media/asl/CA/flask_server.py /var/www/ca

echo "Setup startup"
cp /media/asl/CA/startup.service /etc/systemd/system
mkdir /etc/startup
cp /media/asl/CA/startup /etc/startup
chmod +x /etc/startup/startup
service startup start
systemctl enable startup

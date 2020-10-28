#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 10.0.20.20 netmask 255.255.255.0 up
apt-get install -y openssl
mkdir /etc/ssl/CA
mkdir /etc/ssl/CA/certs
mkdir /etc/ssl/CA/newcerts
mkdir /etc/ssl/CA/private
bash -c "echo '01' > /etc/ssl/CA/serial"
touch /etc/ssl/CA/index.txt
cp /media/asl/CA/openssl.cnf /etc/ssl/
cp /media/asl/CA/cakey.pem /etc/ssl/CA/private
cp /media/asl/CA/cacert.pem /etc/ssl/CA
cp /media/asl/CA/.rnd /home/ubuntu
ip route add 192.168.1.0/24 via 10.0.20.40

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
cp /media/asl/CA/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys
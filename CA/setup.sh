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
<<<<<<< HEAD
echo "10.0.20.10    core" >> /etc/hosts


apt-get update
apt-get install python3-pip -y 
pip3 install Flask

# Internal Firewall
iptables -F
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
iptables -A INPUT -i enp0s10 -j ACCEPT
iptables -A OUTPUT -o enp0s10 -j ACCEPT
iptables -A INPUT -i enp0s3 -s 192.168.1.30 -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -d 192.168.1.30 -p tcp --sport 22 -j ACCEPT
iptables -A INPUT -i enp0s3 -s 10.0.20.10 -p tcp --dport 443 -j ACCEPT
iptables -A OUTPUT -d 10.0.20.10 -o enp0s3 -p tcp --sport 443 -j ACCEPT

# Flask server
mkdir /etc/Flask
mkdir /etc/Flask/private
mkdir /etc/Flask/certs
cp /media/asl/CA/ca_server_cert.pem /etc/Flask/certs/ca_cert.pem
cp /media/asl/CA/ca_server_key.pem /etc/Flask/private/ca_key.pem
cp /media/asl/CA/flask_server.py /home/ubuntu
python3 /home/ubuntu/flask_server.py &

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

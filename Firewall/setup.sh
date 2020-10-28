#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 10.0.20.40 netmask 255.255.255.0 up
ifconfig enp0s8 10.0.10.40 netmask 255.255.255.0 up
ifconfig enp0s9 192.168.1.40 netmask 255.255.255.0 up
iptables -F
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
echo 1 > /proc/sys/net/ipv4/ip_forward
# Allow ssh traffic between VPN Server and Firewall
iptables -A INPUT -i enp0s9 -s 192.168.1.30 -d 192.168.1.40 -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -d 192.168.1.30 -s 192.168.1.40 -p tcp --sport 22 -j ACCEPT
# Allow sftp traffic between Backup Server and Firewall
iptables -A INPUT -i enp0s3 -s 10.0.20.50 -d 10.0.20.40 -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -d 10.0.20.50 -s 10.0.20.40 -p tcp --sport 22 -j ACCEPT
# Allow traffic between Web Server and Core Server
iptables -A FORWARD -i enp0s9 -s 192.168.1.20 -o enp0s8 -d 10.0.10.10 -j ACCEPT
iptables -A FORWARD -i enp0s8 -s 10.0.10.10 -o enp0s9 -d 192.168.1.20 -j ACCEPT
# Allow ssh traffic from VPN Server to any other Server
iptables -A FORWARD -i enp0s9 -s 192.168.1.30 -o enp0s3 -p tcp --dport 22 -j ACCEPT
iptables -A FORWARD -i enp0s3 -p tcp --sport 22 -o enp0s9  -d 192.168.1.30 -j ACCEPT
# Allow sftp traffic between Backup Server and VPN Server
iptables -A FORWARD -i enp0s3 -s 10.0.20.50 -o enp0s9 -d 192.168.1.30 -p tcp --dport 22 -j ACCEPT
iptables -A FORWARD -i enp0s9 -d 10.0.20.50 -o enp0s3 -s 192.168.1.30 -p tcp --sport 22 -j ACCEPT

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
cp /media/asl/Firewall/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys
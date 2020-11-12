#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 192.168.1.30 netmask 255.255.255.0 up
ip route add 10.0.20.0/24 via 192.168.1.40

# Create VPN connection with wireguard
cp /media/asl/VPN/wg_private /home/ubuntu/.ssh/
ip link add wg0 type wireguard
ip addr add 10.0.0.30/24 dev wg0
wg set wg0 listen-port 39198 private-key /home/ubuntu/.ssh/wg_private
ip link set wg0 up
wg set wg0 peer 6ejIgrueSPwWZ9ZFtb0kckmWqHBRctP1fVCb4T6W4yk= allowed-ips 10.0.0.10 endpoint 192.168.1.10:55027
# NAT connection coming from VPN
sysctl -w net.ipv4.ip_forward=1
iptables -A FORWARD -i wg0 -j ACCEPT
iptables -A FORWARD -o wg0 -j ACCEPT
iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE

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
mkdir "/backup_dir"
chown "backup_user" "/backup_dir"
chmod 0703 "/backup_dir"
#SFTP keys for login without password
mkdir /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh
cp /media/asl/VPN/authorized_keys /home/backup_user/.ssh
chmod 755 /home/backup_user/.ssh/authorized_keys
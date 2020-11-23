#!/bin/bash
echo "Setup client"


# Add hosts
echo "192.168.1.20    webserver" >> /etc/hosts
echo "192.168.1.30    vpn" >> /etc/hosts
echo "192.168.1.40    firewall" >> /etc/hosts
echo "10.0.20.10    core" >> /etc/hosts
echo "10.0.20.20    ca" >> /etc/hosts
echo "10.0.20.30    mysql" >> /etc/hosts
echo "10.0.20.50    backup" >> /etc/hosts
echo "nameserver 8.8.8.8" > /etc/resolv.conf

# Create VPN connection with wireguard
cp /media/asl/Client/wg_private /home/ubuntu/.ssh/
chmod 600 /home/ubuntu/.ssh/wg_private
chown ubuntu:root /home/ubuntu/.ssh/wg_private
cp /media/asl/Client/id_rsa /home/ubuntu/.ssh/
chmod 600 /home/ubuntu/.ssh/id_rsa
chown ubuntu:root /home/ubuntu/.ssh/id_rsa
cp /media/asl/Client/id_rsa.pub /home/ubuntu/.ssh/
chmod 644 /home/ubuntu/.ssh/id_rsa.pub
chown ubuntu:root /home/ubuntu/.ssh/id_rsa.pub


# Add CA root cert to trusted cert
cp /media/asl/CA/cacert.pem /home/ubuntu

echo "Setup startup"
cp /media/asl/Client/startup.service /etc/systemd/system
mkdir /etc/startup
cp /media/asl/Client/startup /etc/startup
chmod +x /etc/startup/startup
service startup start
systemctl enable startup
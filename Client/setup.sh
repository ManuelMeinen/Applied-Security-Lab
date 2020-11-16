#!/bin/bash
echo "Setup client"


# Add hosts
echo "192.168.1.20    webserver" >> /etc/hosts
echo "nameserver 8.8.8.8" > /etc/resolv.conf

# Create VPN connection with wireguard
cp /media/asl/Client/wg_private /home/ubuntu/.ssh/

# Add CA root cert to trusted cert
cp /media/asl/CA/cacert.pem /etc/ssl/certs/HomeCA.pem
update-ca-certificates 

echo "Setup startup"
cp /media/asl/Client/startup.service /etc/systemd/system
mkdir /etc/startup
cp /media/asl/Client/startup /etc/startup
chmod +x /etc/setup/startup
service startup start
systemctl enable startup
#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s8 192.168.1.10 netmask 255.255.255.0 up
ip route add 192.168.1.0/24 dev enp0s8

# Add hosts
echo "192.168.1.20    webserver" >> /etc/hosts

# Create VPN connection with wireguard
cp /media/asl/Client/wg_private /home/ubuntu/.ssh/
ip link add wg0 type wireguard
ip addr add 10.0.0.10/24 dev wg0
wg set wg0 listen-port 55027 private-key /home/ubuntu/.ssh/wg_private
ip link set wg0 up
wg set wg0 peer SdVhpKX4AB3tM5kkg8C1MOmWLicx15xv8DjFsh2VJCo= allowed-ips 10.0.0.30,10.0.20.0/24,192.168.1.40 endpoint 192.168.1.30:39198
ip route add 10.0.20.0/24 dev wg0
# Redirect to have ssh on Firewall
ip route add 192.168.1.40/32 dev wg0
# Add CA root cert to trusted cert
cp /media/asl/CA/cacert.pem /etc/ssl/certs/HomeCA.pem
update-ca-certificates 
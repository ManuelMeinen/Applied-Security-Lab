#!/bin/bash
echo "Setup script started..."
ifconfig enp0s3 10.0.20.50 netmask 255.255.255.0 up
ip route add 192.168.1.0/24 via 10.0.20.40

# Do the stuff that only needs to be done when installing
/media/asl/Backup/installation.sh



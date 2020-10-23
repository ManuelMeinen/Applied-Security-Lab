#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 10.0.20.10 netmask 255.255.255.0 up
ifconfig enp0s8 10.0.10.10 netmask 255.255.255.0 up
ip route add 192.168.1.0/24 via 10.0.10.40
ip route add 192.168.1.30/32 via 10.0.20.40
#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 10.0.20.50 netmask 255.255.255.0 up
ip route add 192.168.1.0/24 via 10.0.20.40
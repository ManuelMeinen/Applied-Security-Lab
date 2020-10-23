#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 192.168.1.20 netmask 255.255.255.0 up
ip route add 10.0.10.0/24 via 192.168.1.40
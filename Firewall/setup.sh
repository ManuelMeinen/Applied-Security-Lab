#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 10.0.20.40 netmask 255.255.255.0 up
ifconfig enp0s8 10.0.10.40 netmask 255.255.255.0 up
ifconfig enp0s9 192.168.1.40 netmask 255.255.255.0 up
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
iptables -A INPUT -i enp0s9 -s 192.168.1.30 -d 192.168.1.40 -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -d 192.168.1.30 -s 192.168.1.40 -p tcp --sport 22 -j ACCEPT
iptables -A FORWARD -i enp0s9 -s 192.168.1.20 -o enp0s8 -d 10.0.10.10 -j ACCEPT
iptables -A FORWARD -i enp0s8 -s 10.0.10.10 -o enp0s9 -d 192.168.1.20 -j ACCEPT
iptables -A FORWARD -i enp0s9 -s 192.168.1.30 -o enp0s3 -p tcp --dport 22 -j ACCEPT
iptables -A FORWARD -i enp0s3 -p tcp --sport 22 -o enp0s9  -d 192.168.1.30 -j ACCEPT
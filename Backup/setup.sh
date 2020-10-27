#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 10.0.20.50 netmask 255.255.255.0 up
ip route add 192.168.1.0/24 via 10.0.20.40

# Copy SSH keys to the right directory
cp /media/asl/Backup/backup_sftp_key /home/ubuntu/.ssh/
cp /media/asl/Backup/backup_sftp_key.pub /home/ubuntu/.ssh/
cp /media/asl/Backup/known_hosts /home/ubuntu/.ssh/
chmod 755 /home/ubuntu/.ssh/backup_sftp_key

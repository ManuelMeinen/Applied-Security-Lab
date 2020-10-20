#!/bin/bash
echo "Nothing to be set up..."
ifconfig enp0s3 10.0.20.20 netmask 255.255.255.0 up
apt-get install -y openssl
mkdir /etc/ssl/CA
mkdir /etc/ssl/CA/certs
mkdir /etc/ssl/CA/newcerts
mkdir /etc/ssl/CA/private
bash -c "echo '01' > /etc/ssl/CA/serial"
touch /etc/ssl/CA/index.txt
cp /media/asl/CA/openssl.cnf /etc/ssl/
cp /media/asl/CA/cakey.pem /etc/ssl/CA/private
cp /media/asl/CA/cacert.pem /etc/ssl/CA
cp /media/asl/CA/.rnd /home/ubuntu
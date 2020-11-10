#!/bin/bash
apt-get update
apt install python3-pip -y
pip3 install requests cryptography==3.2.1 Flask
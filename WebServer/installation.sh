#!/bin/bash
apt update 
apt install python3-pip nginx -y
pip3 install requests Flask Flask-WTF email_validator flask-behind-proxy
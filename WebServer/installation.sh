#!/bin/bash
apt update 
apt install nginx -y
apt install python3-pip -y
pip3 install requests Flask Flask-WTF email_validator flask-behind-proxy Flask-Limiter

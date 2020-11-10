#!/bin/bash

# Install dependencies
apt-get update
apt-get install python3-pip -y 
# apt-get install nginx uwsgi uwsgi-plugin-python -y
pip3 install Flask
# pip3 install virtualenv
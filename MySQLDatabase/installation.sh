#!/bin/bash
sudo apt update
sudo apt install mysql-server -y
sudo apt install python3-pip -y
pip3 install Flask
pip3 install mysql-connector-python
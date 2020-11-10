#!/bin/bash

echo "Launching time!"

python3 flask_server.py &
python3 test_server.py &

echo "ENJOY"

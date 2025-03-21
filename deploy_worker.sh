#!/bin/bash

echo "Pulling latest code..."
cd /home/ubuntu/Mail-Worker || exit
git pull origin main

echo "Installing dependencies..."
pip3 install --no-cache-dir -r requirements.txt

echo "Restarting worker service..."
sudo systemctl daemon-reload
sudo systemctl restart worker
sudo systemctl status worker --no-pager

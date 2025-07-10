#!/bin/bash

# Upgrade pip and install requirements
echo "Installing dependencies from requirements-dev.txt..."
pip install --upgrade pip
pip install -r requirements-dev.txt

echo "Dependencies installed successfully."

# Run with: 
# bash setup_scripts/install_req.sh
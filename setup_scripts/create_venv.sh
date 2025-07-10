#!/bin/bash

# Define the virtual environment directory
VENV_DIR="fire-risk-venv"

# Check if the virtual environment already exists
if [ -d "$VENV_DIR" ]; then
  echo "Virtual environment '$VENV_DIR' already exists."
else
  # Create the virtual environment using Python 3
  python3 -m venv "$VENV_DIR"
  if [ $? -eq 0 ]; then
    echo "Virtual environment '$VENV_DIR' created successfully."
  else
    echo "Failed to create virtual environment. Ensure Python 3 and venv module are installed."
    exit 1
  fi
fi

# Run with: 
# bash setup_scripts/link_gcs_with_key.sh


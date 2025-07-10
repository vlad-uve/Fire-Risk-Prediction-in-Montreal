#!/bin/bash
# Link service account key for GCS access

echo "🔐 Linking GCS service account key..."

# Resolve the key path relative to this script's location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KEY_PATH="$SCRIPT_DIR/gcs_service_key.json"

# Export the path
export GOOGLE_APPLICATION_CREDENTIALS="$KEY_PATH"

echo "✅ GCS authentication set using: $GOOGLE_APPLICATION_CREDENTIALS"


# Run with: 
# source setup_scripts/link_gcs_with_key.sh
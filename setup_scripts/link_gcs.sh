#!/bin/bash
# Authenticate GCS if needed

echo "🌐 Running Google Cloud auth setup..."
gcloud auth application-default login

echo "🔗 Setting quota/billing project..."
gcloud auth application-default set-quota-project fire-risk-gcs

echo "✅ GCS linked to your project."

# Run with: 
# bash setup_scripts/link_gcs.sh
# Imports
from google.cloud import storage
from io import BytesIO
import os

def download_data_from_gcs(bucket_name, gcs_files, local_dir='data'):
    """
    Download multiple files from GCS into a local directory.

    Args:
        bucket_name (str): GCS bucket name.
        gcs_files (dict): Mapping of local filenames to GCS paths.
            e.g., {
                'df_fires_history_risk.csv': 'data/df_fires_history_risk.csv',
                'montreal_grid_v1.geojson': 'data/montreal_grid_v1.geojson',
                'xgb_model_v1.pkl': 'model/xgb_model_v1.pkl'
            }
        local_dir (str): Local folder to store the files.
    """
    os.makedirs(local_dir, exist_ok=True)
    client = storage.Client(project="fire-risk-gcs")
    bucket = client.bucket(bucket_name)

    for local_name, gcs_path in gcs_files.items():
        local_path = os.path.join(local_dir, local_name)
        if not os.path.exists(local_path):
            print(f"Downloading {gcs_path} to {local_path}...")
            blob = bucket.blob(gcs_path)
            blob.download_to_filename(local_path)
        else:
            print(f"Already exists locally: {local_path}")
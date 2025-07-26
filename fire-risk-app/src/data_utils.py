# Imports
from google.cloud import storage
import os
import time

def download_data_from_gcs(bucket_name, gcs_files, local_dir='data'):
    """
    Downloads multiple files from a GCS bucket to local paths.

    Args:
        bucket_name (str): Name of the GCS bucket.
        gcs_files (dict): Mapping of local file names to GCS object paths.
        local_dir (str): Root directory to store downloaded files.
    """
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError("❌ GOOGLE_APPLICATION_CREDENTIALS is not set.")

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for local_name, gcs_path in gcs_files.items():
        local_path = os.path.join(local_dir, local_name)

        if not os.path.exists(local_path):
            print(f"⬇️  Downloading {gcs_path} → {local_path}")
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            blob = bucket.blob(gcs_path)

            for attempt in range(3):
                try:
                    blob.download_to_filename(local_path)
                    break
                except Exception as e:
                    if attempt < 2:
                        print(f"🔁 Retrying ({attempt+1}/3): {gcs_path}")
                        time.sleep(1)
                    else:
                        print(f"❌ Failed to download {gcs_path}: {e}")
        else:
            print(f"✅ Already exists: {local_path}")
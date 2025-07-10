from flask import Flask, render_template, url_for, request
from src.data_utils import download_data_from_gcs
from src.model_utils import get_data_for_month, predict_fire_risk
from src.map_utils import fire_risk_to_grid, create_map, plot_risk_to_map
from datetime import datetime
import os
import pandas as pd
import geopandas as gpd
import pickle

app = Flask(__name__, static_folder='static', template_folder='templates')

# Constants
BUCKET_NAME = "fire-risk-gcs-bucket"
LOCAL_DATA_DIR = os.path.join(app.root_path, "data")
DEFAULT_MONTH = "2025-05"

GCS_FILES = {
    "df_fires_history_risk.csv": "data/df_fires_history_risk.csv",
    "montreal_grid_v1.geojson": "data/montreal_grid_v1.geojson",
    "xgb_model_v1.pkl": "model/xgb_model_v1.pkl"
}

# Download files from GCS only once at startup
print("Checking and downloading required files from GCS...")
download_data_from_gcs(BUCKET_NAME, GCS_FILES, LOCAL_DATA_DIR)

# Load data and model from local disk
print("Loading data and model from disk...")
df_fires_history_risk = pd.read_csv(os.path.join(LOCAL_DATA_DIR, "df_fires_history_risk.csv"))
gpd_grid = gpd.read_file(os.path.join(LOCAL_DATA_DIR, "montreal_grid_v1.geojson"))
with open(os.path.join(LOCAL_DATA_DIR, "xgb_model_v1.pkl"), "rb") as f:
    xgb_model = pickle.load(f)
print("Initialization complete.")

# --- Main route ---
@app.route('/', methods=['GET', 'POST'])
def show_maps():
    try:
        # Get selected month from form or use default
        selected_month = request.form['month'] if request.method == 'POST' else DEFAULT_MONTH
        readable_month = datetime.strptime(selected_month, "%Y-%m").strftime("%B %Y")

        # Predict fire risk for the selected month
        X_month, y_true = get_data_for_month(df_fires_history_risk, selected_month)
        y_pred = predict_fire_risk(X_month, y_true, xgb_model)

        # Assign prediction to gpd grid
        grid_pred = fire_risk_to_grid(y_pred, gpd_grid)
        grid_true = fire_risk_to_grid(y_true, gpd_grid)

        # Save maps to static folder
        static_map_dir = os.path.join(app.root_path, 'static', 'maps')
        os.makedirs(static_map_dir, exist_ok=True)

        plot_risk_to_map(create_map(), grid_pred).save(os.path.join(static_map_dir, 'map_month_pred.html'))
        plot_risk_to_map(create_map(), grid_true).save(os.path.join(static_map_dir, 'map_month_true.html'))

        return render_template(
            "maps.html",
            pred_map_url=url_for('static', filename='maps/map_month_pred.html'),
            true_map_url=url_for('static', filename='maps/map_month_true.html'),
            month=selected_month,
            readable_month=readable_month
        )

    except Exception as e:
        return f"<h2>Error: {str(e)}</h2>", 500

if __name__ == '__main__':
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug_mode)
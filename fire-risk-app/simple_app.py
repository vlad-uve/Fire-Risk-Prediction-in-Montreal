from flask import Flask, render_template, url_for, request, send_from_directory
from src.model_utils import get_data_for_month, predict_fire_risk
from src.map_utils import fire_risk_to_grid, create_map, plot_risk_to_map
from datetime import datetime
import os
import pandas as pd
import geopandas as gpd
import pickle
import xgboost as xgb

# --- App setup ---
app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Constants ---
LOCAL_DATA_DIR = os.path.join(app.root_path, "data")
LOCAL_MODEL_DIR = os.path.join(app.root_path, "model")
DEFAULT_MONTH = "2025-05"
STATIC_MAP_DIR = os.path.join(app.root_path, "static", "maps")
TMP_MAP_DIR = "/tmp/maps"

df_fires_history_risk = None
gpd_grid = None
xgb_model = None
data_loaded = False
model_loaded = False

# --- Routes ---
def ensure_data_loaded():
    global data_loaded, df_fires_history_risk, gpd_grid
    if not data_loaded:
        print("Loading data on first request...")
        df_fires_history_risk = pd.read_csv(os.path.join(LOCAL_DATA_DIR, "df_fires_history_risk.csv"))
        gpd_grid = gpd.read_file(os.path.join(LOCAL_DATA_DIR, "montreal_grid_v1.geojson"))
        data_loaded = True
        print("Data loaded.")


def ensure_model_loaded():
    global model_loaded, xgb_model
    if not model_loaded:
        print("Loading model on first request...")
        with open(os.path.join(LOCAL_MODEL_DIR, "xgb_model_v1.pkl"), "rb") as f:
            xgb_model = pickle.load(f)
        model_loaded = True
        print("Model loaded.")


@app.route('/', methods=['GET', 'POST'])
def show_maps():
    try:
        # Ensure data and model loading at cold run
        ensure_data_loaded()
        ensure_model_loaded()

        # Get selected month from form or use default
        selected_month = request.form['month'] if request.method == 'POST' else DEFAULT_MONTH
        readable_month = datetime.strptime(selected_month, "%Y-%m").strftime("%B %Y")

        pred_map_url = None
        true_map_url = None

        if df_fires_history_risk is not None and not df_fires_history_risk.empty:
            if selected_month == DEFAULT_MONTH:
                true_map_url = url_for('static', filename='maps/default_true_map.html')
                pred_map_url = url_for('static', filename='maps/default_pred_map.html')
            else:
                # Get true and predicted fire risk data for the selected month
                X_month, y_true = get_data_for_month(df_fires_history_risk, selected_month)
                y_pred = predict_fire_risk(X_month, y_true, xgb_model)

                # Assign true and prediction to gpd grid
                grid_true = fire_risk_to_grid(y_true, gpd_grid)
                grid_pred = fire_risk_to_grid(y_pred, gpd_grid)
                
                # Save true and predicted maps to temp folder
                os.makedirs(TMP_MAP_DIR, exist_ok=True)
                dynamic_true_map_path = os.path.join(TMP_MAP_DIR, 'map_month_true.html')
                dynamic_pred_map_path = os.path.join(TMP_MAP_DIR, 'map_month_pred.html')
                
                plot_risk_to_map(create_map(), grid_true).save(dynamic_true_map_path)
                plot_risk_to_map(create_map(), grid_pred).save(dynamic_pred_map_path)

                true_map_url = url_for('serve_dynamic_true_map')
                pred_map_url = url_for('serve_dynamic_pred_map')
                

        return render_template(
            "maps.html",
            pred_map_url=pred_map_url,
            true_map_url=true_map_url,
            month=selected_month,
            readable_month=readable_month
        )

    except Exception as e:
        return f"<h2>Error: {str(e)}</h2>", 500

@app.route('/map_true')
def serve_dynamic_true_map():
    return send_from_directory(TMP_MAP_DIR, 'map_month_true.html')

@app.route('/map_pred')
def serve_dynamic_pred_map():
    return send_from_directory(TMP_MAP_DIR, 'map_month_pred.html')

if __name__ == '__main__':
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug_mode)

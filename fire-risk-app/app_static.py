# app_static.py – using static data and model files
from flask import Flask, render_template, url_for, request, send_from_directory
from src.model_utils import get_data_for_month, predict_fire_risk
from src.map_utils import fire_risk_to_grid, create_map, plot_risk_to_map
from datetime import datetime
import os
import pandas as pd
import geopandas as gpd
import pickle
import xgboost as xgb

# ------------------------------------------------------------------------------
# 1) Flask setup, paths and constants
# ------------------------------------------------------------------------------
app = Flask(__name__, static_folder='static', template_folder='templates')

LOCAL_DATA_DIR  = os.path.join(app.root_path, "data")
LOCAL_MODEL_DIR = os.path.join(app.root_path, "model")
DEFAULT_MONTH = "2025-05"
TMP_MAP_DIR = "/tmp/maps"  # Render allows writing only here
DEFAULT_TRUE_HTML = "maps/default_true_map.html"
DEFAULT_PRED_HTML = "maps/default_pred_map.html"

# ------------------------------------------------------------------------------
# 2) Lazy loading on first request
# ------------------------------------------------------------------------------
df_fires_history_risk = None
gpd_grid              = None
xgb_model             = None
data_loaded           = False
model_loaded          = False

def ensure_data_loaded():
    global data_loaded, df_fires_history_risk, gpd_grid
    if data_loaded:
        return
    print("Loading CSV & GeoJSON…")
    df_fires_history_risk = pd.read_csv(
        os.path.join(LOCAL_DATA_DIR, "df_fires_history_risk.csv")
    )
    gpd_grid = gpd.read_file(
        os.path.join(LOCAL_DATA_DIR, "montreal_grid_v1.geojson")
    )
    data_loaded = True
    print("✅ Data loaded.")

def ensure_model_loaded():
    global model_loaded, xgb_model
    if model_loaded:
        return
    print("Loading model…")
    with open(os.path.join(LOCAL_MODEL_DIR, "xgb_model_v1.pkl"), "rb") as f:
        xgb_model = pickle.load(f)
    model_loaded = True
    print("✅ Model loaded.")

# ------------------------------------------------------------------------------
# 3) Main route
# ------------------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def show_maps():
    try:
        # Ensure data and model are loaded into memory
        ensure_data_loaded()
        ensure_model_loaded()

        # Determine selected month
        selected_month = (
            request.form["month"] if request.method == "POST" else DEFAULT_MONTH
        )
        readable_month = datetime.strptime(
            selected_month, "%Y-%m"
        ).strftime("%B %Y")

        # If default month, load pre-rendered static maps
        if selected_month == DEFAULT_MONTH:
            true_map_url = url_for("static", filename=DEFAULT_TRUE_HTML)
            pred_map_url = url_for("static", filename=DEFAULT_PRED_HTML)

        else:
            # For other months, run prediction pipeline

            # Filter true data and predict fire risk
            X_month, y_true = get_data_for_month(
                df_fires_history_risk, selected_month
            )
            y_pred    = predict_fire_risk(X_month, y_true, xgb_model)

            # Join true and predictions with grid GeoDataFrame
            grid_true = fire_risk_to_grid(y_true, gpd_grid)
            grid_pred = fire_risk_to_grid(y_pred, gpd_grid)

            # Generate map HTML files in /tmp
            os.makedirs(TMP_MAP_DIR, exist_ok=True)
            true_path = os.path.join(TMP_MAP_DIR, "map_month_true.html")
            pred_path = os.path.join(TMP_MAP_DIR, "map_month_pred.html")

            plot_risk_to_map(create_map(), grid_true).save(true_path)
            plot_risk_to_map(create_map(), grid_pred).save(pred_path)

            # Set dynamic map URLs (served via Flask routes)
            true_map_url = url_for("serve_dynamic_true_map")
            pred_map_url = url_for("serve_dynamic_pred_map")

        # Render the map viewer template with variables
        return render_template(
            "maps.html",
            pred_map_url=pred_map_url,
            true_map_url=true_map_url,
            month=selected_month,
            readable_month=readable_month,
        )

    except Exception as e:
        # Error fallback with exception reporting
        return f"<h2>Error: {e}</h2>", 500

# ------------------------------------------------------------------------------
# 4) Serve dynamic maps
# ------------------------------------------------------------------------------
@app.route('/map_true')
def serve_dynamic_true_map():
    return send_from_directory(TMP_MAP_DIR, 'map_month_true.html')

@app.route('/map_pred')
def serve_dynamic_pred_map():
    return send_from_directory(TMP_MAP_DIR, 'map_month_pred.html')

# ------------------------------------------------------------------------------
# 5) Entrypoint
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_ENV") == "development",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
    )

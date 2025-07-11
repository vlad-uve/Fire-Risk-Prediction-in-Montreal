from flask import Flask, render_template, url_for, request, send_from_directory
from src.model_utils import get_data_for_month
from src.map_utils import fire_risk_to_grid, create_map, plot_risk_to_map
from datetime import datetime
import os
import pandas as pd
import geopandas as gpd

# --- App setup ---
app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Constants ---
LOCAL_DATA_DIR = os.path.join(app.root_path, "data")
DEFAULT_MONTH = "2025-05"
STATIC_MAP_DIR = os.path.join(app.root_path, "static", "maps")
TMP_MAP_DIR = "/tmp/maps"

df_fires_history_risk = None
gpd_grid = None
data_loaded = False

# --- Routes ---
def ensure_data_loaded():
    global data_loaded, df_fires_history_risk, gpd_grid
    if not data_loaded:
        print("Loading data on first request...")
        df_fires_history_risk = pd.read_csv(os.path.join(LOCAL_DATA_DIR, "df_fires_history_risk.csv"))
        gpd_grid = gpd.read_file(os.path.join(LOCAL_DATA_DIR, "montreal_grid_v1.geojson"))
        data_loaded = True
        print("Data loaded.")

@app.route('/', methods=['GET', 'POST'])
def show_maps():
    try:
        ensure_data_loaded()

        selected_month = request.form['month'] if request.method == 'POST' else DEFAULT_MONTH
        readable_month = datetime.strptime(selected_month, "%Y-%m").strftime("%B %Y")

        pred_map_url = "https://via.placeholder.com/800x600?text=Predicted+Map"
        true_map_url = None
        show_true_map = False

        if df_fires_history_risk is not None and not df_fires_history_risk.empty:
            if selected_month == DEFAULT_MONTH:
                true_map_url = url_for('static', filename='maps/default_true_map.html')
                show_true_map = True
            else:
                X_month, y_true = get_data_for_month(df_fires_history_risk, selected_month)
                grid_true = fire_risk_to_grid(y_true, gpd_grid)
                os.makedirs(TMP_MAP_DIR, exist_ok=True)
                dynamic_map_path = os.path.join(TMP_MAP_DIR, 'map_month_true.html')
                plot_risk_to_map(create_map(), grid_true).save(dynamic_map_path)
                true_map_url = url_for('serve_dynamic_true_map')
                show_true_map = True

        # Always render index.html but pass show_true_map flag
        return render_template(
            "index.html",
            pred_map_url=pred_map_url,
            true_map_url=true_map_url,
            month=selected_month,
            readable_month=readable_month,
            show_true_map=show_true_map  # Pass the new flag!
        )

    except Exception as e:
        return f"<h2>Error: {str(e)}</h2>", 500

@app.route('/map_true')
def serve_dynamic_true_map():
    return send_from_directory(TMP_MAP_DIR, 'map_month_true.html')

if __name__ == '__main__':
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug_mode)

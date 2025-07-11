from flask import Flask, render_template, url_for, request
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

# --- Load data ---
print("Loading data...")
df_fires_history_risk = pd.read_csv(os.path.join(LOCAL_DATA_DIR, "df_fires_history_risk.csv"))
gpd_grid = gpd.read_file(os.path.join(LOCAL_DATA_DIR, "montreal_grid_v1.geojson"))
print("Data loaded.")

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def show_maps():
    try:
        selected_month = request.form['month'] if request.method == 'POST' else DEFAULT_MONTH
        readable_month = datetime.strptime(selected_month, "%Y-%m").strftime("%B %Y")

        # Filter dummy data for the month
        X_month, y_true = get_data_for_month(df_fires_history_risk, selected_month)
        grid_true = fire_risk_to_grid(y_true, gpd_grid)

        # Save true map only
        static_map_dir = os.path.join(app.root_path, 'static', 'maps')
        os.makedirs(static_map_dir, exist_ok=True)

        true_map_path = os.path.join(static_map_dir, 'map_month_true.html')
        plot_risk_to_map(create_map(), grid_true).save(true_map_path)

        return render_template(
            "maps.html",
            pred_map_url="https://via.placeholder.com/800x600?text=Predicted+Map",
            true_map_url=url_for('static', filename='maps/map_month_true.html'),
            month=selected_month,
            readable_month=readable_month
        )

    except Exception as e:
        return f"<h2>Error: {str(e)}</h2>", 500

# --- Main ---
if __name__ == '__main__':
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug_mode)
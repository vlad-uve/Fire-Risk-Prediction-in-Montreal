# Imports
import folium
import geopandas as gpd
import pandas as pd


def fire_risk_to_grid(y_data, gpd_grid):
    """
    Merge fire risk predictions with spatial grid.

    Args:
        y_data (pd.Series): Predicted fire risk values (0 or 1) indexed by GRID_ID.
        gpd_grid (GeoDataFrame): Spatial grid with 'GRID_ID' as index or column.

    Returns:
        GeoDataFrame: Grid with 'RISK_NEXT_MONTH' column (values: 'low', 'high').
    """
    # Map numeric predictions to risk labels and merge with grid
    risk_labels = y_data.map({0: 'low', 1: 'high'})
    gpd_grid_risk = gpd_grid.merge(risk_labels.rename('RISK_NEXT_MONTH'), on='GRID_ID', how='left')

    # Fill missing values with 'low' risk
    gpd_grid_risk = gpd_grid_risk.fillna('low')

    # Ensure GRID_ID is a column
    gpd_grid_risk['GRID_ID'] = gpd_grid_risk.index

    return gpd_grid_risk


def create_map():
    """
    Create a base folium map centered on Montreal.

    Returns:
        folium.Map: Initialized map with bounding box and zoom settings.
    """
    m = folium.Map(
        location=[45.55, -73.6],
        zoom_start=11,
        width='100%',
        height='580px'
    )
    m.fit_bounds([[45.4, -73.9], [45.7, -73.4]])
    m.options['minZoom'] = 10
    m.options['maxBounds'] = [[45.35, -74.0], [45.75, -73.2]]
    return m


def plot_risk_to_map(map_obj, gpd_grid_risk, risk_colors={'low': '#fecc5c', 'high': '#bd0026'}):
    """
    Overlay fire risk grid on a folium map.

    Args:
        map_obj (folium.Map): Map to add GeoJson layer to.
        gpd_grid_risk (GeoDataFrame): Grid with fire risk classification.
        risk_colors (dict): Color mapping for risk levels.

    Returns:
        folium.Map: Map with the risk grid overlay.
    """
    folium.GeoJson(
        gpd_grid_risk,
        style_function=lambda feature: {
            'fillColor': risk_colors.get(feature['properties']['RISK_NEXT_MONTH'], '#cccccc'),
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7,
        },
        tooltip=folium.GeoJsonTooltip(fields=['GRID_ID', 'RISK_NEXT_MONTH'])
    ).add_to(map_obj)

    return map_obj
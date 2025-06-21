from flask import Flask, render_template

import folium
import json


app = Flask(__name__)


@app.route("/map")
def map_grid():

    # Create a map centered on Montreal
    m = folium.Map(location=[45.55, -73.6], zoom_start=11)

    # Lock map to specific bounds (Montreal Island approx)
    m.fit_bounds([[45.4, -73.9], [45.7, -73.4]])
    m.options['minZoom'] = 10
    m.options['maxBounds'] = [[45.35, -74.0], [45.75, -73.2]]

    # read grid data
    with open('app/data/montreal_grid_v1.geojson') as f:
        grid_data = json.load(f)

    folium.GeoJson(
        grid_data,
        name="Fire Risk Grid",
        style_function=lambda x: {
            'fillColor': '#fecc5c',
            'color': '#000000',
            'weight': 1,
            'fillOpacity': 0.3,
        },
        tooltip=folium.GeoJsonTooltip(fields=['GRID_ID'])
    ).add_to(m)        

    return render_template("map.html", map=m._repr_html_())


if __name__ == "__main__":
    app.run(debug=True)

import geopandas as gpd
from keplergl import KeplerGl

gdf = gpd.read_file("Centros Comerciales.kml")
gdf.head()

# Initialize a Kepler.gl map
map_1 = KeplerGl(height=600)

# Add a dataset (e.g., GeoJSON or Pandas DataFrame)
map_1.add_data(data=gdf, name="My Data")

# Define the latitude, longitude, and zoom level for centering
center_lat = -2.1409155511014633  # Replace with your latitude
center_lon = -79.90951320936493  # Replace with your longitude
zoom_level = 10  # Adjust zoom level as needed

# Update the map configuration to center it
config = {
    "mapState": {
        "bearing": 0,
        "latitude": center_lat,
        "longitude": center_lon,
        "pitch": 0,
        "zoom": zoom_level
    }
}

# Apply the configuration to the map
map_1.config = config

map_1.save_to_html(file_name="kepler_map2.html")

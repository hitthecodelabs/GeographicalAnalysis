import math
import geopandas as gpd

from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.tile_providers import get_provider, Vendors

def latlon_to_web_mercator(lat, lon):
    """
    Convert latitude and longitude to Web Mercator projection.
    """
    k = 6378137  # Earth's radius in meters
    x = lon * (k * math.pi / 180.0)
    y = math.log(math.tan((90 + lat) * math.pi / 360.0)) * k
    return x, y

# Extract x and y coordinates for polygons, ignoring z-coordinate
def extract_coords(geometry):
    if geometry.geom_type == "Polygon":
        # Extract x, y from 3D coordinates
        coords = [(coord[0], coord[1]) for coord in geometry.exterior.coords]
    elif geometry.geom_type == "MultiPolygon":
        # Handle MultiPolygons by extracting all exterior rings
        coords = [(coord[0], coord[1]) for polygon in geometry for coord in polygon.exterior.coords]
    else:
        coords = []  # Handle unsupported geometries gracefully
    return coords

# Load GeoPandas DataFrame
gdf = gpd.read_file("Centros Comerciales.kml")
gdf.head()

# Extract coordinates and convert to Web Mercator
gdf["xs"] = gdf.geometry.apply(
    lambda geom: [latlon_to_web_mercator(lat, lon)[0] for lon, lat in extract_coords(geom)]
)
gdf["ys"] = gdf.geometry.apply(
    lambda geom: [latlon_to_web_mercator(lat, lon)[1] for lon, lat in extract_coords(geom)]
)

# Create a Bokeh ColumnDataSource
source = ColumnDataSource({
    "xs": gdf["xs"],
    "ys": gdf["ys"],
    "name": gdf["Name"],  # Add additional columns if needed
})

# Center of the map
lat = -2.1409155511014633
lon = -79.90951320936493

# Convert lat/lon to Web Mercator coordinates
center_x, center_y = latlon_to_web_mercator(lat, lon)

# Define zoom level
zoom_level = 16  # Higher zoom level = closer view
tile_size = 256  # Tile size for Web Mercator
earth_circumference = 40075016.686  # Earth's circumference in meters
initial_resolution = earth_circumference / tile_size  # Resolution at zoom level 0
resolution = initial_resolution / (2 ** zoom_level)  # Resolution at the desired zoom level

# Calculate x_range and y_range based on zoom level
range_size = resolution * tile_size  # Size of the range in meters
x_range = (center_x - range_size / 2, center_x + range_size / 2)
y_range = (center_y - range_size / 2, center_y + range_size / 2)

# Define the map with centered coordinates and zoom level
p = figure(
    x_range=x_range,
    y_range=y_range,
    x_axis_type="mercator",
    y_axis_type="mercator",
    title=f"Map with GeoPandas Data (Zoom Level {zoom_level})"
)

# tile_provider = get_provider(Vendors.ESRI_IMAGERY)  # Using ESRI Satellite Imagery
tile_provider = get_provider(Vendors.OSM)  # Using Open Street Maps contributors
p.add_tile(tile_provider)

# Plot polygons
p.patches(xs="xs", ys="ys", source=source, fill_alpha=0.5, line_width=1, color="blue")

n = 7
output_file(f"map_debug{n}.html")

# Show the map
show(p)

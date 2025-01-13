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

lat = -2.1409155511014633
lon = -79.90951320936493

# Convert lat/lon to Web Mercator coordinates
center_x, center_y = latlon_to_web_mercator(lat, lon)

# Define the map with centered coordinates
p = figure(
    x_range=(center_x - 50000, center_x + 50000),  # Adjust the range for zoom level
    y_range=(center_y - 50000, center_y + 50000),  # Adjust the range for zoom level
    x_axis_type="mercator",
    y_axis_type="mercator",
    title="Map with GeoPandas Data"
)

tile_provider = get_provider(Vendors.CARTODBPOSITRON)
p.add_tile(tile_provider)

# Plot polygons
p.patches(xs="xs", ys="ys", source=source, fill_alpha=0.5, line_width=1, color="blue")

output_file("map_debug5.html")

# Show the map
show(p)

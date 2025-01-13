import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go

# Mapbox Access Token
mapbox_token = ""
px.set_mapbox_access_token(mapbox_token)

gdf = gpd.read_file("Centros Comerciales.kml")
gdf = set_elevation_column(gdf, column_name='DN', num_elevations=1, min_elevation=50, max_elevation=300)
gdf

coords = list(gdf.geometry.iloc[0].boundary.coords)
coords

lat_c, lon_c = list(gdf.geometry.iloc[0].centroid.coords)[0][::-1]
lat_c, lon_c

# Example Data for Polygons (Deforestation Polygons)
polygon_data = {
    "lat": [i[1] for i in coords],
    "lon": [i[0] for i in coords],
    "category": ["Deforestation"]*len(coords)
}

# Convert to DataFrame
polygon_df = pd.DataFrame(polygon_data)
polygon_df

# Center Coordinates
center_coordinates = {"lat": lat_c, "lon": lon_c}
center_coordinates

# Create the Figure
fig = go.Figure()

# Add the Polygon as a Line
fig.add_trace(
    go.Scattermapbox(
        lat=polygon_data["lat"],
        lon=polygon_data["lon"],
        mode="lines",  # Draw as lines
        line=dict(width=2, color="red"),  # Line style
        name="Deforestation Polygon"
    )
)

# Mapbox Settings
fig.update_layout(
    mapbox=dict(
        accesstoken=mapbox_token,
        style="satellite",  # Custom Style URL
        center=center_coordinates,
        zoom=16.5
    ),
    # title="Deforestation Polygon",
    title=f"Polygon",
    width=1250,  # Set the width of the figure
    height=715,   # Set the height of the figure
    margin=dict(l=0, r=0, t=0, b=0)  # Remove margins
)

# Save as PNG
fig.write_image("map_polygon.png")

# Show the Map
fig.show()

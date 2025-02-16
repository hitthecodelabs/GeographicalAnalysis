import os
import geopandas as gpd

from glob import glob
from fastkml import kml
from shapely.geometry import mapping
from shapely.geometry import Polygon, MultiPolygon

def geojson_2_kml(input_geojson, output_kml):
    """
    Converts a GeoJSON file into a KML file using GeoPandas.

    Parameters:
    input_geojson (str): Path to the input GeoJSON file.
    output_kml (str): Path to the output KML file where the converted data will be saved.

    This function reads a GeoJSON file using GeoPandas and saves it as a KML file,
    leveraging GeoPandas' built-in support for KML format.
    """
    # Load the GeoJSON file into a GeoDataFrame
    gdf = gpd.read_file(input_geojson)
    
    # Save as KML file
    gdf.to_file(output_kml, driver="KML")
    
    print(f"KML file saved: {output_kml}")

def geojson_to_kml(input_geojson, output_kml):
    """
    Converts a GeoJSON file into a KML file.

    Parameters:
    input_geojson (str): Path to the input GeoJSON file.
    output_kml (str): Path to the output KML file where the converted data will be saved.

    This function reads a GeoJSON file using GeoPandas, extracts its geometries,
    and creates a corresponding KML file using the fastkml library. If a 'name' 
    attribute exists in the GeoJSON, it is assigned as the name of the corresponding
    KML Placemark; otherwise, the default name is 'Unnamed'.
    """
    # Load the GeoJSON file into a GeoDataFrame
    gdf = gpd.read_file(input_geojson)
    
    # Create a KML object
    k = kml.KML()
    doc = kml.Document()
    k.append(doc)
    
    # Iterate through the GeoDataFrame and convert each feature
    for _, row in gdf.iterrows():
        placemark = kml.Placemark()
        placemark.geometry = row.geometry
        placemark.name = row.get('name', 'Unnamed')  # Use 'name' field if available
        doc.append(placemark)
    
    # Write the KML to a file
    with open(output_kml, 'w', encoding='utf-8') as f:
        f.write(k.to_string(prettyprint=True))
    
    print(f"KML file saved: {output_kml}")

def filter_polygons(gdf, threshold=83):
    """
    Filters polygons where any coordinate (latitude or longitude) is equal to or less than the given threshold.

    Parameters:
    gdf (GeoDataFrame): GeoDataFrame containing geometries.
    threshold (float): The threshold value to filter coordinates.

    Returns:
    GeoDataFrame: Filtered GeoDataFrame.
    """
    def check_polygon(geom):
        """Check if any coordinate in the polygon meets the threshold condition."""
        if isinstance(geom, (Polygon, MultiPolygon)):
            for polygon in geom.geoms if isinstance(geom, MultiPolygon) else [geom]:
                for x, y, *_ in polygon.exterior.coords:
                    if x <= threshold or y <= threshold:  # Check both lat and lon
                        return False
        return True

    return gdf[gdf['geometry'].apply(check_polygon)]

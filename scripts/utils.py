import os
import geopandas as gpd

from glob import glob
from fastkml import kml
from shapely.geometry import mapping
from shapely.geometry import Polygon, MultiPolygon

def display_directory_structure(root_dir, indent=""):
    """
    Recursively generates and prints a formatted directory structure.

    Parameters:
    root_dir (str): The root directory to scan.
    indent (str): The indentation level for formatting.
    """
    print(f"\n{root_dir}")
    
    def get_structure(dir_path, current_indent):
        try:
            items = sorted(os.listdir(dir_path))
            for index, item in enumerate(items):
                item_path = os.path.join(dir_path, item)
                prefix = "├── " if index < len(items) - 1 else "└── "
                print(f"{current_indent}{prefix}{item}")
                if os.path.isdir(item_path) and "site-packages" not in item_path:
                    get_structure(item_path, current_indent + "│   " if index < len(items) - 1 else current_indent + "    ")
        except PermissionError:
            print(f"{current_indent}└── [Permission Denied]")

    get_structure(root_dir, indent)

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

def filter_polygons(gdf, lon_threshold=-82):
    """
    Filters polygons where the longitude is greater than or equal to a given threshold.

    Parameters:
    gdf (GeoDataFrame): GeoDataFrame containing geometries.
    lon_threshold (float): The minimum longitude value to keep polygons.

    Returns:
    GeoDataFrame: Filtered GeoDataFrame.
    """
    def filter_by_longitude(geom):
        """Checks if a geometry meets the longitude threshold."""
        if isinstance(geom, (Polygon, MultiPolygon)):
            for polygon in geom.geoms if isinstance(geom, MultiPolygon) else [geom]:
                for x, y, *_ in polygon.exterior.coords:
                    if x >= lon_threshold:
                        return True
        return False

def gdf_to_kml(gdf, output_kml):
    """
    Converts a GeoDataFrame into a KML file using the fastkml library.

    Parameters:
    gdf (GeoDataFrame): GeoDataFrame containing geometries.
    output_kml (str): Path to the output KML file where the converted data will be saved.
    """
    k = kml.KML()
    doc = kml.Document()
    k.append(doc)
    
    for _, row in gdf.iterrows():
        placemark = kml.Placemark()
        placemark.geometry = row.geometry
        placemark.name = row.get('name', 'Unnamed')
        doc.append(placemark)
    
    with open(output_kml, 'w', encoding='utf-8') as f:
        f.write(k.to_string(prettyprint=True))
    
    print(f"KML file saved: {output_kml}")

def convert_to_parquet(input_file):
    """
    Convert a KML or GeoJSON file to a Parquet file.
    
    Parameters:
    input_file (str): Path to the input KML or GeoJSON file.
    
    Returns:
    None: Saves the output as a Parquet file in the same directory as the input file.
    """
    output_file = input_file.replace(".kml", ".parquet").replace(".geojson", ".parquet")
    gdf = gpd.read_file(input_file)
    gdf.to_parquet(output_file, compression='snappy')
    print(f"Converted {input_file} to {output_file}")

# Benchmark Load Time and Query Time
def benchmark_spatial_query(target_file, reference_file, use_parquet=False):
    target_gdf = gpd.read_file(target_file)
    target_geom = target_gdf.unary_union
    
    start_time = time.time()
    if use_parquet:
        reference_gdf = gpd.read_parquet(reference_file)
    else:
        reference_gdf = gpd.read_file(reference_file)
    load_time = time.time() - start_time
    
    start_query = time.time()
    intersecting_polygons = reference_gdf[reference_gdf.intersects(target_geom)]
    query_time = time.time() - start_query
    
    print(f"Load Time ({'Parquet' if use_parquet else 'KML/GeoJSON'}): {load_time:.4f} sec")
    print(f"Query Time ({'Parquet' if use_parquet else 'KML/GeoJSON'}): {query_time:.4f} sec")
    print(f"Intersecting Polygons: {len(intersecting_polygons)}")

import os
import fiona
import shutil
import pyproj

import zipfile
import numpy as np
import geopandas as gpd

from glob import glob
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from shapely.geometry import Polygon


def unzip_file(zip_path, extract_to):
    """
    Extracts a ZIP file to the specified folder.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def convert_kmz_to_kml(kmz_file_path):
    """
    Converts a KMZ file to a KML file by extracting its internal KML file.
    """
    if not os.path.exists(kmz_file_path):
        raise FileNotFoundError(f"File not found: {kmz_file_path}")

    kml_file_path = os.path.splitext(kmz_file_path)[0] + ".kml"

    with zipfile.ZipFile(kmz_file_path, 'r') as kmz:
        for file_name in kmz.namelist():
            if file_name.endswith('.kml'):
                with kmz.open(file_name) as kml_file:
                    with open(kml_file_path, 'wb') as output_kml:
                        output_kml.write(kml_file.read())
                return kml_file_path

    raise ValueError("No KML file found inside the KMZ.")


def read_kml(file_path):
    """
    Reads a KML file into a GeoDataFrame.
    """
    fiona.drvsupport.supported_drivers['KML'] = 'rw'

    if file_path.endswith('.kmz'):
        with zipfile.ZipFile(file_path, 'r') as kmz:
            kmz.extractall('temp_kml')
        file_path = glob('temp_kml/*.kml')[0]

    with fiona.open(file_path, driver='KML') as src:
        features = list(src)

    gdf = gpd.GeoDataFrame.from_features(features)

    if os.path.exists('temp_kml'):
        shutil.rmtree('temp_kml')

    return gdf, features


def validate_coordinates(coord_list):
    """
    Validates and classifies coordinates as Decimal Degrees (DD) or UTM.
    """
    results = []
    for lat, lon in coord_list:
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            results.append((lat, lon, 'DD'))
        elif 100000 <= lat <= 10000000 and 0 <= lon <= 834000:
            results.append((lat, lon, 'UTM'))
        else:
            results.append((lat, lon, 'Unknown'))
    return results


def calculate_area_hectares(geometry):
    """
    Calculates the area of a geometry in hectares.
    """
    proj = pyproj.Proj(proj="utm", zone=17, ellps="WGS84", south=True)

    utm_coords = [proj(*coord) for coord in geometry.exterior.coords]
    polygon = Polygon(utm_coords)
    area_sq_meters = polygon.area
    return area_sq_meters / 1e4


def calculate_polygon_area(file_path):
    """
    Reads a KML or KMZ file, calculates polygon areas in hectares, and returns a GeoDataFrame.
    """
    gdf, _ = read_kml(file_path)
    gdf["area_ha"] = gdf.geometry.apply(calculate_area_hectares)
    return gdf


def string_similarity(a, b):
    """
    Calculates similarity ratio between two strings.
    """
    return SequenceMatcher(None, a, b).ratio()


def add_attribute_to_geojson(geojson_file, attribute_key, attribute_value, output_file):
    """
    Adds an attribute to each feature in a GeoJSON file and saves the updated file.
    """
    gdf = gpd.read_file(geojson_file)
    gdf[attribute_key] = attribute_value
    gdf.to_file(output_file, driver='GeoJSON')

def generate_html_map(gdf, output_folder, start_index=0, end_index=None):
    """
    Generates HTML maps for polygons in a GeoDataFrame.

    Parameters:
        gdf (GeoDataFrame): Input GeoDataFrame with geometries.
        output_folder (str): Folder to save the HTML files.
        start_index (int): Starting index of polygons to process.
        end_index (int): Ending index of polygons to process.

    Returns:
        None
    """
    os.makedirs(output_folder, exist_ok=True)

    end_index = end_index or gdf.shape[0]

    for i in range(start_index, end_index):
        gdff = gdf.iloc[i]
        polygon = gdff.geometry
        name = gdff.get("Name", f"Polygon_{i}")
        HA = gdff.get("ha", "Unknown")
        desc = gdff.get("Description", "")

        if len(str(desc)) < 15:
            desc = ""

        lon, lat = list(polygon.centroid.coords)[0]

        # Create a map centered on the location of the polygon
        m = folium.Map(location=[lat, lon], zoom_start=18)

        # Add ESRI World Imagery basemap
        esri_world_imagery = folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='ESRI World Imagery',
            name='ESRI World Imagery',
            overlay=False,
            control=True
        )
        esri_world_imagery.add_to(m)

        # Add polygon to the map
        folium.GeoJson(polygon).add_to(m)

        # Add a title to the map
        title_html = f'''
            <h3 align="center" style="font-size:20px"><b>Polygon {i+1} |{desc}| {name} - {HA} HA</b></h3>
        '''
        m.get_root().html.add_child(folium.Element(title_html))

        # Add layer control
        folium.LayerControl().add_to(m)

        # Save the map as an HTML file
        map_file = os.path.join(output_folder, f"{name}.html")
        m.save(map_file)

        print(f"Generated map for Polygon {i+1}: {name} ({HA} HA)")

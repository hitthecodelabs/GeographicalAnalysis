import geopandas as gpd
import time
import argparse

def benchmark_spatial_query(target_file, reference_file, use_parquet=False):
    """
    Loads target and reference polygons, then benchmarks spatial queries.
    """
    # Load the target polygon
    target_gdf = gpd.read_file(target_file)
    target_geom = target_gdf.unary_union  # Merge multiple geometries if needed
    
    # Load the reference dataset
    start_time = time.time()
    if use_parquet:
        reference_gdf = gpd.read_parquet(reference_file)
    else:
        reference_gdf = gpd.read_file(reference_file)
    load_time = time.time() - start_time
    
    # Perform spatial intersection
    start_query = time.time()
    intersecting_polygons = reference_gdf[reference_gdf.intersects(target_geom)]
    query_time = time.time() - start_query
    
    print(f"Load Time ({'Parquet' if use_parquet else 'KML/GeoJSON'}): {load_time:.4f} seconds")
    print(f"Query Time ({'Parquet' if use_parquet else 'KML/GeoJSON'}): {query_time:.4f} seconds")
    print(f"Intersecting Polygons: {len(intersecting_polygons)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark KML/GeoJSON vs. Parquet for spatial queries")
    parser.add_argument("target_file", help="Path to the target polygon KML or GeoJSON")
    parser.add_argument("reference_file", help="Path to the reference polygons KML, GeoJSON, or Parquet")
    parser.add_argument("--parquet", action="store_true", help="Use Parquet for reference dataset")
    
    args = parser.parse_args()
    benchmark_spatial_query(args.target_file, args.reference_file, use_parquet=args.parquet)

import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import time

class GeolocateMarkers:
    def __init__(self, districts, gdf):
        print('Initializing GeolocateMarkers...')
        self.districts = districts
        self.gdf = gdf

    def locate_points(self, output_file):
        print('Locating points...')
        df = pd.DataFrame(columns=['id','category','name','street', 'number','zipcode','district', 'latitude', 'longitude'])
        rows = []
        
        for _, row_geo in self.gdf.iterrows():
            polygon = row_geo['geometry']
            for _, row_district in self.districts.iterrows():
                polygon_district = row_district['geometry']
                if polygon.intersects(polygon_district):
                    rows.append([row_geo['osm_id'],row_geo['shop'],row_geo['name'], row_geo['addr:street'], row_geo['addr:housenumber'], row_geo['addr:postcode'], row_district['NOMBRE'], polygon.centroid.y, polygon.centroid.x])
                    break
        df = pd.DataFrame(rows, columns=['id','category','name','street', 'number','zipcode','district', 'latitude', 'longitude'])
        df.to_csv(output_file, index=False)
            

if __name__ == "__main__":
    districts = gpd.read_file('../data/gjson/distritos.geojson')
    
    print('Reading GeoJSON...')
    start_time = time.time()
    gdf = gpd.read_file('../data/gpkg/json/building.json')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('GeoJSON read in {:.2f} seconds'.format(elapsed_time))
    
    geolocator = GeolocateMarkers(districts, gdf)
    geolocator.locate_points('../data/points/building.csv')
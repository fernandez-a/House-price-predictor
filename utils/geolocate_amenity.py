import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import time

class GeolocateAmenity:
    def __init__(self, districts, gdf):
        print('Initializing GeolocateMarkers...')
        self.districts = districts
        self.gdf = gdf

    def locate_points(self):
        print('Locating points...')
        df = pd.DataFrame(columns=['id','category','brand','name','street', 'number','zipcode','district', 'latitude', 'longitude'])
        rows = []
        
        for _, row_geo in self.gdf.iterrows():
            polygon = row_geo['geometry']
            for _, row_district in self.districts.iterrows():
                polygon_district = row_district['geometry']
                if polygon.intersects(polygon_district):
                    rows.append([row_geo['osm_id'],row_geo['amenity'],row_geo['brand'],row_geo['name'], row_geo['addr:street'], row_geo['addr:housenumber'], row_geo['addr:postcode'], row_district['NOMBRE'], polygon.centroid.y, polygon.centroid.x])
                    break
        df = pd.DataFrame(rows, columns=['id','category','brand','name','street', 'number','zipcode','district', 'latitude', 'longitude'])
        return df
            

if __name__ == "__main__":
    districts = gpd.read_file('../data/gjson/distritos.geojson')
    df = []
    final_df = pd.DataFrame()
    print('Reading GeoJSON...')
    for i in range(0,17):
        start_time = time.time()
        print(f'Part {i}...')
        gdf = gpd.read_file(f'../data/gpkg/json/amenity_fixed/part_{i}.geojson')
        end_time = time.time()
        elapsed_time = end_time - start_time
        print('GeoJSON read in {:.2f} seconds'.format(elapsed_time))
        
        geolocator = GeolocateAmenity(districts, gdf)
        df.append(geolocator.locate_points())
        print(f'Part {i} done')

    final_df = pd.concat(df)
    final_df.to_csv('../data/points/amenity_1.csv', index=False)